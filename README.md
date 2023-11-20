# MC-LARC

## ChatGPT4-32k_wrong_output_description_generator.py

To run this program, you need **API-KEY** and **AZURE_OPENAI_ENDPOINT**.
</br></br>
In the ChatGPT4-32k_wrong_output_description_generator.py,
</br></br>
```python
# OpenAI API key setting
openai.api_type = "azure"
openai.api_base = "AZURE_OPENAI_ENDPOINT"   # Here
openai.api_key = "API-KEY"                  # Here
openai.api_version = "2023-05-15"
```

</br></br>
By running this Python program, you can create a MC-LARC_description_output.csv file that includes one correct answer choice and four incorrect answer choices.
</br></br>
And run the program,
- Check_format.py
</br>
to check the wrong format descriptions.

</br></br>
You need to check the wrongly generated task IDs due to the issue of GPT in the ChatGPT4_error_log folder. And then regenerate them.