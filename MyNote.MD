## Setting up the Virtual Environment etc under Windows

My method for running under windows is based on a conversation with Gemeni Pro AI is as follwos. (I had all manner of requirements issues trying to run without virtual env.)

Enter The Following Commands which is generally as listed in README.MD but with minor additions and tweaks.

```
python -m venv myLlmTestenv
 myLlmTestenv\Scripts\activate
 python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```
Also I found because I am in Windows and Michael uses a Mac there is an issue ref Windows using CRLF and MAC using just LF.  So enter this command to set this repository to use LF like what one does on a Mac.

```
git config core.autocrlf input 
```
Then add a .gitignore file similar to this

```
myLlmTestenv/
src/__pycache__/
myLlmTestenv
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
Question to ponder: why am I no longer getting messenges about OpenAI not connected when using Local LLM?  Maybe the issue was to do with the crlf/lf issue.
