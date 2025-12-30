"""Utilitas kontrol konkurensi (versi optimasi)

Perbaikan:
1. Batas konkurensi dinamis berdasarkan beban sistem
2. Pengendalian terpisah per jenis verifikasi
3. Mendukung tingkat konkurensi yang lebih tinggi
4. Pemantauan beban dan penyesuaian otomatis
"""
import asyncio
import logging
from typing import Dict
import psutil

logger = logging.getLogger(__name__)

# Hitung batas konkurensi maksimal secara dinamis
def _calculate_max_concurrency() -> int:
    """Hitung batas konkurensi berdasarkan sumber daya sistem"""
    try:
        cpu_count = psutil.cpu_count() or 4
        memory_gb = psutil.virtual_memory().total / (1024 ** 3)
        
        # Hitung berdasarkan CPU dan memori
        # Setiap inti CPU mendukung 3-5 tugas paralel
        # Setiap GB memori mendukung 2 tugas paralel
        cpu_based = cpu_count * 4
        memory_based = int(memory_gb * 2)
        
        # Ambil nilai minimum keduanya lalu batasi rentang
        max_concurrent = min(cpu_based, memory_based)
        max_concurrent = max(10, min(max_concurrent, 100))  # gunakan rentang 10-100
        
        logger.info(
            f"Sumber daya sistem: CPU={cpu_count}, Memori={memory_gb:.1f}GB, "
            f"Batas paralel dihitung={max_concurrent}"
        )
        
        return max_concurrent
        
    except Exception as e:
        logger.warning(f"Gagal membaca informasi sumber daya: {e}, menggunakan nilai default")
        return 20  # Nilai default

# Hitung batas per jenis verifikasi
_base_concurrency = _calculate_max_concurrency()

# Buat semaphore terpisah untuk tiap jenis verifikasi
# Menghindari satu jenis memblokir jenis lainnya
_verification_semaphores: Dict[str, asyncio.Semaphore] = {
    "gemini_one_pro": asyncio.Semaphore(_base_concurrency // 5),
    "chatgpt_teacher_k12": asyncio.Semaphore(_base_concurrency // 5),
    "spotify_student": asyncio.Semaphore(_base_concurrency // 5),
    "youtube_student": asyncio.Semaphore(_base_concurrency // 5),
    "bolt_teacher": asyncio.Semaphore(_base_concurrency // 5),
}


def get_verification_semaphore(verification_type: str) -> asyncio.Semaphore:
    """Dapatkan semaphore untuk jenis verifikasi tertentu
    
    Args:
        verification_type: jenis verifikasi
        
    Returns:
        asyncio.Semaphore: semaphore yang digunakan
    """
    semaphore = _verification_semaphores.get(verification_type)
    
    if semaphore is None:
        # Jika jenis tidak dikenal, buat semaphore default
        semaphore = asyncio.Semaphore(_base_concurrency // 3)
        _verification_semaphores[verification_type] = semaphore
        logger.info(
            f"Membuat semaphore baru untuk jenis {verification_type}: "
            f"limit={_base_concurrency // 3}"
        )
    
    return semaphore


def get_concurrency_stats() -> Dict[str, Dict[str, int]]:
    """Ambil statistik konkurensi
    
    Returns:
        dict: info paralel untuk tiap jenis
    """
    stats = {}
    for vtype, semaphore in _verification_semaphores.items():
        # Catatan: _value adalah atribut internal yang dapat berubah antar versi Python
        try:
            available = semaphore._value if hasattr(semaphore, '_value') else 0
            limit = _base_concurrency // 3
            in_use = limit - available
        except Exception:
            available = 0
            limit = _base_concurrency // 3
            in_use = 0
        
        stats[vtype] = {
            'limit': limit,
            'in_use': in_use,
            'available': available,
        }
    
    return stats


async def monitor_system_load() -> Dict[str, float]:
    """Pantau beban sistem
    
    Returns:
        dict: informasi beban sistem
    """
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_percent = psutil.virtual_memory().percent
        
        return {
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            'concurrency_limit': _base_concurrency,
        }
    except Exception as e:
        logger.error(f"Gagal memantau beban sistem: {e}")
        return {
            'cpu_percent': 0.0,
            'memory_percent': 0.0,
            'concurrency_limit': _base_concurrency,
        }


def adjust_concurrency_limits(multiplier: float = 1.0):
    """Sesuaikan batas konkurensi secara dinamis
    
    Args:
        multiplier: faktor penyesuaian (0.5-2.0)
    """
    global _verification_semaphores, _base_concurrency
    
    # Batasi rentang faktor
    multiplier = max(0.5, min(multiplier, 2.0))
    
    new_base = int(_base_concurrency * multiplier)
    new_limit = max(5, min(new_base // 3, 50))  # Setiap jenis berada pada rentang 5-50
    
    logger.info(
        f"Menyesuaikan batas konkurensi: multiplier={multiplier}, "
        f"new_base={new_base}, per_type={new_limit}"
    )
    
    # Buat semaphore baru
    for vtype in _verification_semaphores.keys():
        _verification_semaphores[vtype] = asyncio.Semaphore(new_limit)


# Tugas pemantauan beban
_monitor_task = None

async def start_load_monitoring(interval: float = 60.0):
    """Mulai tugas pemantauan beban
    
    Args:
        interval: jeda pemantauan (detik)
    """
    global _monitor_task
    
    if _monitor_task is not None:
        return
    
    async def monitor_loop():
        while True:
            try:
                await asyncio.sleep(interval)
                
                load_info = await monitor_system_load()
                cpu = load_info['cpu_percent']
                memory = load_info['memory_percent']
                
                logger.info(
                    f"Beban sistem: CPU={cpu:.1f}%, Memori={memory:.1f}%"
                )
                
                # Sesuaikan batas konkurensi secara otomatis
                if cpu > 80 or memory > 85:
                    # Jika beban tinggi, turunkan batas
                    adjust_concurrency_limits(0.7)
                    logger.warning("Beban sistem tinggi, menurunkan batas konkurensi")
                elif cpu < 40 and memory < 60:
                    # Jika beban rendah, tingkatkan batas
                    adjust_concurrency_limits(1.2)
                    logger.info("Beban sistem rendah, menaikkan batas konkurensi")
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Pemantauan beban mengalami kesalahan: {e}")
    
    _monitor_task = asyncio.create_task(monitor_loop())
    logger.info(f"Pemantauan beban dimulai: interval={interval}s")


async def stop_load_monitoring():
    """Hentikan tugas pemantauan"""
    global _monitor_task
    
    if _monitor_task is not None:
        _monitor_task.cancel()
        try:
            await _monitor_task
        except asyncio.CancelledError:
            pass
        _monitor_task = None
        logger.info("Pemantauan beban dihentikan")
