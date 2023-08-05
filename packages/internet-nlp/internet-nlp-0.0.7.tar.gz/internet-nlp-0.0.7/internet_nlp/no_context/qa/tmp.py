import NoContextQA

tmp = NoContextQA.NoContextQA()
tmp.setQuestion("Who is the richest person in the world")
tmp.setResponse("")
tmp.doAllCommands()
print(tmp.getAnswer())
