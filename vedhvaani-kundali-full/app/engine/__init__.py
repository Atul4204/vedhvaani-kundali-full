from .safe_engine import compute_all_safe
try:
    from .swe_engine import compute_all_swe
except Exception:
    # SWE not available
    def compute_all_swe(*args, **kwargs):
        raise RuntimeError('pyswisseph not available')
