from queue import Queue

from bears.php.PHPCodeBeautifierBear import PHPCodeBeautifierBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper, \
    execute_bear

from coalib.settings.Section import Section
from coala_utils.ContextManagers import prepare_file

in_file = """<?php
$var = false;
echo $var;
>
"""

out_file = """<?php
$var = false;
echo $var;
>
"""

simplify_in_file = """<?php
$var = true;
if ($var == FALSE){
    echo 'hi';
}
>
"""

simplify_out_file = """<?php
$var = true;
if ($var == false){
    echo 'hi';
}
>
"""


class PHPCodeBeautifierBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('')
        self.uut = PHPCodeBeautifierBear(self.section, Queue())

    def test_without_simplify(self):
        content = in_file.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                fdict = {fname: file}
                results[0].apply(fdict)
                self.assertEqual(''.join(fdict[fname]), out_file)

    def test_with_simplify(self):
        content = simplify_in_file.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                fdict = {fname: file}
                results[0].apply(fdict)
                self.assertEqual(''.join(fdict[fname]), simplify_out_file)
