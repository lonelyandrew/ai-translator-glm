# ai-translator

1. 在`env_template.txt`中填写OPENAI相关配置信息，然后将其改名为`.env`，
2. 命令行运行翻译程序运行脚本`ai_translator.sh`，相关参数可以通过修改命令行参数来实现，
3. 图像界面程序通过运行脚本`start_streamlit.sh`来启动一个Streamlit应用来实现，启动后浏览器会打开对应的页面

优化点:
1. 添加了翻译目标语言(`target_lang`)的参数；
2. 修改了prompt，将表格翻译的实现思路改为json翻译，更容易保持原始的表格结构；
3. 添加了Streamlit界面，对用户更友好;
4. 优化了Writer的格式呈现，进行了分行和PDF表格问题的修复。