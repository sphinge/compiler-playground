# import io
# import sys

# from main import main


# def test_main():
#     # Capture the output of the main function
#     captured_output = io.StringIO()
#     sys.stdout = captured_output

#     main()  # Call your main function

#     sys.stdout = sys.__stdout__  # Reset the standard output to its original value

#     # Assert that the function prints out the correct string
#     assert captured_output.getvalue().strip() == "Hello World!"
