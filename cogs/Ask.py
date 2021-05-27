import discord
import os
import time
from discord.ext import commands
import requests as rq

class Ask(commands.Cog):
  
  def __init__(self, client):
    self.client = client
  
  # defining some variables
  categories = [
    'Any',
    'Linux',
    'DevOps',
    'Networking',
    'PHP',
    'JS',
    'Python',
    'Bash',
    'SQL',
    'code',
    'Cloud',
    'Docker',
    'Kubernetes',
  ]
  difficulties = [
    'Any', 
    'Easy', 
    'Medium', 
    'Hard']
  
  API_TOKEN = os.environ['API_TOKEN']

  # variable declarations
  timer = 90
  quiztime = '02/02/21'
  category = categories[0]
  difficulty = difficulties[0]
  limit = 1
  response = ''

  #Events
  @commands.Cog.listener()
  async def on_ready(self):
    print('Cog is online')

  # Commands
  # @commands.command()
  # async def ping(self, ctx):
  #   await ctx.send('4 packets recieved gracefully in ' + str(round(commands.client.latency, 4)) + 'ms')

  # packages question only
  def packageQuestion(self, debugmode=False):
    question = self.response.json()[0]['question']
    return f'\n{question}'

  # packages correct answers only
  def packageCorrectAnswers(self, debugmode=False):
    options = []
    correct_answers = self.response.json()[0]['correct_answers']
    answers = self.response.json()[0]['answers']
    for keys in correct_answers.keys():
      if correct_answers[keys] == 'true':
        options.append(answers[keys[:8]])
  
    packagedAnswers = ''
    for option in range(len(options)):
      packagedAnswers += '\n ' + str(option + 1) + '. ' + options[option]
    return 'The correct answer(s) were:\n' + packagedAnswers

  # packages options only with response input and string output
  def packageOptions(self, debugmode=False):
    options = []
    answers = self.response.json()[0]['answers']
    for keys in answers.keys():
      if answers[keys] is not None:
        options.append(answers[keys])

    packagedOptions = '\nThe options are:'
    for option in range(len(options)):
      packagedOptions += '\n' + str(option + 1) + '. ' + options[option]
    return packagedOptions

  # method to split json to strings
  def packageQuestionJson(self, debugmode=False):
    message = self.packageQuestion(self.response)
    message += self.packageOptions(self.response)
    message += '\nCategory: '
    message += self.response.json()[0]['category']
    message += '\nDifficulty: '
    message += self.response.json()[0]['difficulty']
    return message

  # method to call API and get JSON info
  def getQuestions(self):
    auth = {'X-Api-Key': self.API_TOKEN, 'content-type': 'application/json'}
    params = {'limit': 1}
    if self.category != self.categories[0]:
      params['category'] = self.category
    if self.difficulty != self.difficulties[0]:
      params['difficulty'] = self.difficulty
    self.response = rq.get(f"https://quizapi.io/api/v1/questions", headers=auth, json=params)
    return self.packageQuestionJson(self.response)

  # sends message in a cleaner embed format
  def sendAsEmbed(self, Title, Description, Footer):
    embed = discord.Embed(title=Title, description = Description, color=0xFF5733)
    embed.set_footer(text = Footer)
    return embed

  # invokes a loop which sends answers after questions after seconds seconds
  async def looptime(self, ctx, seconds, question, answer):
    start_time = time.time()
    await ctx.send(embed=self.sendAsEmbed('Question', question, f'Answers in {seconds} seconds!'))
    while True:
      current_time = time.time()
      elapsed_time = current_time - start_time
      if elapsed_time > seconds:
        logtext = "Finished iterating in: " + str(int(elapsed_time))  + " seconds"
        await ctx.send(embed=self.sendAsEmbed('Quiz time\'s up!', answer, logtext))
        break

  # tests loop feature
  @commands.command()
  async def testloop(self, ctx):
    await self.looptime(ctx, 10, 'This is a test question', 'This is a test answer')

  # asks question
  @commands.command()
  async def testnow(self, ctx):
    await ctx.send(embed = self.sendAsEmbed('The technical question for this week is:' ,self.getQuestions(), 'Use `answer` to get answer or use asknow for automatic answer'))

  # reveals answer and ends session
  @commands.command()
  async def answer(self, ctx):
    await ctx.send(embed = self.sendAsEmbed('Answering time is over!' ,self.packageCorrectAnswers(self.response),'gg'))
  
  # asks the questions
  @commands.command(pass_context=True)
  async def asknow(self, ctx):
    await self.looptime(ctx, 10, self.getQuestions(), self.packageCorrectAnswers())

def setup(client):
  client.add_cog(Ask(client))
