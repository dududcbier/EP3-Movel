from textwrap import fill
import re
import pprint as pp
import numpy
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import filemapper as fm

routers = ['EpidemicRouter', 'ProphetRouter', 'SprayAndWaitRouter']
bufferSize = ['1M', '10M', '100M']
nodes = ['50', '100']
types = ['bikes', 'cars']

def bargraph(what, t, pos, data, unit=None):
	print(routers, data)
	fig = plt.figure()
	plt.bar(pos, data[0], 1, label='1MB')
	plt.bar([p + 1 for p in pos], data[1], 1, label='10MB')
	plt.bar([p + 2 for p in pos], data[2], 1, label='100MB')
	plt.legend(title='Tamanho do buffer:')
	plt.xticks([p + 1 for p in pos], routers)
	title = what + " usando o cenário"
	if (t == 'cars'): 
		title = title + " 1 e "
	else: 
		title = title + " 2 e "
	if (n == '50'): 
		title = title + "metade do número de nós para diferentes roteamentos com tamanhos variados de buffer"
	else:
		title = title + "número de nós padrão para diferentes roteamentos com tamanhos variados de buffer"
	plt.title(fill(title))
	plt.xlabel("Roteamento")
	if (unit != None):
		plt.ylabel(what + " (" + unit + ")")
	else:
		plt.ylabel(what)
	plt.tight_layout()
	try:
		plt.savefig('./graphs/router_impact/' + t + '/' + what + '/' + n)
	except FileNotFoundError:
		os.makedirs('./graphs/router_impact/' + t + '/' + what + '/')
		plt.savefig('./graphs/router_impact/' + t + '/' + what + '/' + n)
	plt.close(fig)


results = {'cars': {}, 'bikes': {}}
for t in types:
	results[t] = {}
	for r in routers:
		results[t][r] = {}
		for bs in bufferSize:
			results[t][r][bs] = {}
			for n in nodes:
				results[t][r][bs][n] = {}

# Read data 
for t in types:
	res = results[t]
	files = fm.load(t)
	for f in files:
		r, bs, n, _ = f.split('_') # Getting the result's parameters
		for line in fm.read(f):
			try:
				stat, value = line.split(':')
				value = float(value)
				res[r][bs][n][stat] = value
			except ValueError:
				pass

# Router Impact
for t in types:
	for n in nodes:
		delivery_probs = []
		latency_avgs = []
		overhead_ratio = []
		hopcount_avg = []
		for bs in bufferSize:
			dp = []
			la = []
			oh = []
			ha = []
			for r in routers:
				dp.append(round(results[t][r][bs][n]['delivery_prob'] * 100, 1))
				la.append(results[t][r][bs][n]['latency_avg'])
				oh.append(results[t][r][bs][n]['overhead_ratio'])
				ha.append(results[t][r][bs][n]['hopcount_avg'])
			delivery_probs.append(dp)
			latency_avgs.append(la)
			overhead_ratio.append(oh)
			hopcount_avg.append(ha)
		pos = [0, 3.5, 7]
		bargraph("Probabilidade de entrega", t, pos, delivery_probs, unit='%')
		bargraph("Latência", t, pos, latency_avgs, unit='s')
		bargraph("Overhead", t, pos, overhead_ratio)
		bargraph("Média de saltos", t, pos, hopcount_avg)
