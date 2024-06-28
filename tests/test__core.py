from agogos._core import _Block, _Base, _SequentialSystem, _ParallelSystem
from tests.util import remove_cache_files
from pathlib import Path


class Test_Base:
    def test_init(self):
        base = _Base()
        assert base is not None

    def test_get_hash(self):
        assert _Base().get_hash() == "e75c7852dd3d36ffc2f1b90efa9568d8"

    def test_set_hash(self):
        base = _Base()
        prev_hash = base.get_hash()
        base._set_hash("prev_hash")
        assert base.get_hash() != prev_hash

    def test_get_children(self):
        base = _Base()
        assert base.get_children() == []

    def test_get_parent(self):
        base = _Base()
        assert base.get_parent() is None

    def test__set_parent(self):
        base = _Base()
        base._set_parent(base)
        assert base.get_parent() == base

    def test__set_children(self):
        base = _Base()
        base._set_children([base])
        assert base.get_children() == [base]

    def test__repr_html_(self):
        base = _Base()
        assert (
            base._repr_html_()
            == "<div style='border: 1px solid black; padding: 10px;'><p><strong>Class:</strong> _Base</p><ul><li><strong>Hash:</strong> e75c7852dd3d36ffc2f1b90efa9568d8</li><li><strong>Parent:</strong> None</li><li><strong>Children:</strong> None</li></ul></div>"
        )

    def test_save_to_html(self):
        html_path = Path("./tests/cache/test_html.html")
        Path("./tests/cache/").mkdir(parents=True, exist_ok=True)
        base = _Base()
        base.save_to_html(html_path)
        assert Path.exists(html_path)
        remove_cache_files()


class TestBlock:
    def test_block_init(self):
        block = _Block()
        assert block is not None

    def test_block_set_hash(self):
        block = _Block()
        block._set_hash("")
        hash1 = block.get_hash()
        assert hash1 == "8c52898e95f367f12e9079cc62d141cb"
        block._set_hash(hash1)
        hash2 = block.get_hash()
        assert hash2 == "243051d47d23a36250057824eed90525"
        assert hash1 != hash2

    def test_block_get_hash(self):
        block = _Block()
        block._set_hash("")
        hash1 = block.get_hash()
        assert hash1 == "8c52898e95f367f12e9079cc62d141cb"

    def test__repr_html_(self):
        block_instance = _Block()

        html_representation = block_instance._repr_html_()

        assert html_representation is not None


class TestSequentialSystem:
    def test_system_init(self):
        system = _SequentialSystem()
        assert system is not None

    def test_system_hash_no_steps(self):
        system = _SequentialSystem()
        assert system.get_hash() == ""

    def test_system_hash_with_1_step(self):
        block1 = _Block()

        system = _SequentialSystem([block1])
        assert system.get_hash() == "8c52898e95f367f12e9079cc62d141cb"
        assert block1.get_hash() == system.get_hash()

    def test_system_hash_with_2_steps(self):
        block1 = _Block()
        block2 = _Block()

        system = _SequentialSystem([block1, block2])
        assert system.get_hash() != block1.get_hash()
        assert (
            system.get_hash() == block2.get_hash() == "a60a4a1d474b8454b0ee9197875171f6"
        )

    def test_system_hash_with_3_steps(self):
        block1 = _Block()
        block2 = _Block()
        block3 = _Block()

        system = _SequentialSystem([block1, block2, block3])
        assert system.get_hash() != block1.get_hash()
        assert system.get_hash() != block2.get_hash()
        assert block1.get_hash() != block2.get_hash()
        assert (
            system.get_hash() == block3.get_hash() == "dfebfe0e709805bd8bc328d115400929"
        )

    def test__repr_html_(self):
        block_instance = _Block()
        system_instance = _SequentialSystem([block_instance, block_instance])
        html_representation = system_instance._repr_html_()

        assert html_representation is not None


class TestParallelSystem:
    def test_parallel_system_init(self):
        parallel_system = _ParallelSystem()
        assert parallel_system is not None

    def test_parallel_system_hash_no_steps(self):
        system = _ParallelSystem()
        assert system.get_hash() == ""

    def test_parallel_system_hash_with_1_step(self):
        block1 = _Block()

        system = _ParallelSystem([block1])
        assert system.get_hash() == "8c52898e95f367f12e9079cc62d141cb"
        assert block1.get_hash() == system.get_hash()

    def test_parallel_system_hash_with_2_steps(self):
        block1 = _Block()
        block2 = _Block()

        system = _ParallelSystem([block1, block2])
        assert system.get_hash() != block1.get_hash()
        assert block1.get_hash() == block2.get_hash()
        assert system.get_hash() != block2.get_hash()
        assert system.get_hash() == "6430f15bf7782822914896704610d45d"

    def test_parallel_system_hash_with_3_steps(self):
        block1 = _Block()
        block2 = _Block()
        block3 = _Block()

        system = _ParallelSystem([block1, block2, block3])
        assert system.get_hash() != block1.get_hash()
        assert system.get_hash() != block2.get_hash()
        assert system.get_hash() != block3.get_hash()
        assert block1.get_hash() == block2.get_hash() == block3.get_hash()
        assert system.get_hash() == "e4e48c6863f83ed0e876357da5a6ed24"

    def test_parallel_system__repr_html_(self):
        block_instance = _Block()
        system_instance = _ParallelSystem([block_instance, block_instance])
        html_representation = system_instance._repr_html_()

        assert html_representation is not None
