import streamlit as st
from app.utils import parse_function_definition, generate_test_inputs

def main():
    st.title("Aegis Test")
    st.write("A simple tool for generating and testing Python functions.")

    code = st.text_area("Enter Python code:", height=200)

    num_tests = st.slider("Number of Test Cases", min_value=1, max_value=50, value=10)
    int_min = st.number_input("Integer Range (Min)", value=-100)
    int_max = st.number_input("Integer Range (Max)", value=100)
    float_min = st.number_input("Float Range (Min)", value=-10.0)
    float_max = st.number_input("Float Range (Max)", value=10.0)
    string_length = st.slider("String Length", min_value=1, max_value=50, value=10)

    if code:
        try:
            function_name, parameters = parse_function_definition(code)
            if function_name:
                st.success(f"Function Name: {function_name}")
                st.write("Parameters:")
                for param in parameters:
                    st.write(f"- {param['name']}: {param['type']}")

                test_inputs = generate_test_inputs(parameters,
                                                   num_tests=num_tests,
                                                   int_range=(int_min, int_max),
                                                   float_range=(float_min, float_max),
                                                   string_length=string_length)
                st.write("Generated Test Inputs:")
                for i, inputs in enumerate(test_inputs):
                    st.write(f"**Test Case {i+1}:**")
                    st.json(inputs)
            else:
                st.error("No function definition found in the code.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()