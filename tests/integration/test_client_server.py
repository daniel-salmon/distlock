import subprocess

from distlock import Distlock


def test_create_lock_delete_lock(distlock_server: subprocess.Popen) -> None:
    distlock = Distlock()
    distlock.create_lock("key")
    distlock.delete_lock("key")
    locks = distlock.list_locks()
    lock_names = {lock.key for lock in locks}
    assert "key" not in lock_names
