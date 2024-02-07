from ezCcompiler import Compiler

TEST_FILE_DIR = "tests/files/"
TEST_FILE_PAIRS = [
    ["input_1.ezC", "output_1.c"],
    ["fibonacci.ezC", "fibonacci.c"],
    # ["input_3.ezC", "output_3.c"],
]


def test_compiler():
    for [input_filename, output_filename] in TEST_FILE_PAIRS:
        input_content = open(TEST_FILE_DIR + input_filename).read()
        expected_output = open(TEST_FILE_DIR + output_filename).read()
        compiled_output = Compiler.run_deterministically(input_content)

        # TEST DEBUGGING
        # with open(TEST_FILE_DIR + "FOO1.c", "w") as output:
        #     output.write(expected_output)
        # with open(TEST_FILE_DIR + "FOO2.c", "w") as output:
        #     output.write(compiled_output)
        assert compiled_output == expected_output
