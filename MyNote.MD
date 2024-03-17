## Notes on This Fork From Michaels LLM Tester

# Setting up the Vertual Environment

My method based on a conversation with Gemeni Pro is as follwos. (This is for on Windows)

Enter The Following Commands which is generally as listed in README.md

```
python -m venv myLlmTestenv
 myLlmTestenv\Scripts\activate
 python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```
Also I found because I am in Windows and Michael uses a Mac there is an issue ref Windows using CRLF and MAC using just Line feed.

So enter this command to set this repository to use LF like waht one does OnaMac.

```
git config core.autocrlf input 
```


Now adjust the screen size in config.yaml to significantly less than the size of your screem and the LLM parameters to what you prefer/Require.
In my case I choose:

```
base_url: 'http://localhost:1234/v1'
api_key: 'not-needed'
questions_file: 'LLM Test.md'
system_prompt: 'You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful.'
temperature: 0.2
font_size: 18
window_size: [1800, 900]
```

Now install and set up LM Studio and set up the local Inference server.

Then Make any changes required to the questions in the "LLM Test.md".

Then run tester with
```
python main.py
```
Question why am I getting messenges about OpenAI not connected when using Local LLM?

Tried putting in an OpenAI code....
