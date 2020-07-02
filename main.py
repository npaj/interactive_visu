import os 
import argparse

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import pandas as pd
from numpy.fft import fft
import numpy as np
import scipy.signal as sig

import sounddevice as sd

parser = argparse.ArgumentParser()

parser.add_argument('--datapath', type=str, required=True)
parser.add_argument('--metadatapath', type=str, required=True)

parser.add_argument('--fs', type=int, required=False, default=500000)
parser.add_argument('--sound', type=bool, required=False, default=False)

args = parser.parse_args()

soundPath = args.datapath
info = pd.read_csv(args.metadatapath)
playSound = args.sound
FS = args.fs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }}

app.layout = html.Div([
    html.Div(
        dcc.Graph(id='3Demb', 
        figure = {
        'data': [go.Scatter(
            x = info['x'],
            y = info['y'],
            
            mode = 'markers',
            text=['target : {} <br>filename : {}'.format(info['target'][k], info['filename'][k]) for k in range(len(info))],
            marker=dict(size = 15,
                color=info['target'],
                colorscale='jet',
                showscale=True,
                line_width=1,
                colorbar=dict(
                thicknessmode = 'fraction',
                thickness=0.01,
                xanchor = 'center')))],
           'layout': dict(title='emb',
                xaxis_title="",
                yaxis_title="",
                height=1000,
                scene = dict(zaxis = dict(
                title='amb')))}), style={'width': '100%'}),
            dcc.Markdown('''
                    [lien projet](nn)
                        ''', id = 'MC'),
            dcc.Graph(id = 'signal'),
            dcc.Graph(id = 'fft'),
            dcc.Graph(id = 'stft')], 
        style={'columnCount': 2}  )


@app.callback(Output('signal', 'figure'),
    [Input('3Demb', 'clickData')])
def time(clickData):
    sound = info['filename'][clickData['points'][0]['pointIndex']]
    print(sound)
    x = np.loadtxt(os.path.join(soundPath, sound))
    N = len(x)

    if playSound:
        sd.play(sig.tukey(N,0.1)*x/x.max(), 10000)

    return {
        'data': [go.Scatter(
                    x = np.arange(len(x))/FS*1e3, 
                    y = x)],
        'layout': dict(xaxis = {'title': 'Temps [ms]'},
                        yaxis = {'title': 'Amplitude'},
                        height=320)}

@app.callback(Output('fft', 'figure'),
    [Input('3Demb', 'clickData')])
def fft_dispay(clickData):
    sound = info['filename'][clickData['points'][0]['pointIndex']]
    x = np.loadtxt(os.path.join(soundPath, sound))
    N = len(x)
    return {
        'data': [go.Scatter(
                        x = np.arange(len(x))*FS/N, 
                        y = 20*np.log10(np.abs(fft(x))))],
        'layout': dict(xaxis = {'title': 'Fréquence [Hz]', 'range' : [1, 6],'type':'log'},
                        yaxis = {'title': 'DSP'},height=320)}

@app.callback(Output('stft', 'figure'),
    [Input('3Demb', 'clickData')])
def stft(clickData):
    sound = info['filename'][clickData['points'][0]['pointIndex']]
    x = np.loadtxt(os.path.join(soundPath, sound))
    N = len(x)
    WW = 128
    f,t_,Zxx = sig.stft(x,fs = FS,window = 'hann', nperseg = WW,noverlap = int(3/4*WW),return_onesided=True)
    N = len(x)
    return {
    'data': [go.Heatmap(
                    x = t_*1e3, y = f, z=np.abs(Zxx))],
    'layout': dict(yaxis = {'title': 'Fréquence Hz', 'type' : 'log'},
                    xaxis = {'title': 'Temps [ms]'},
                    height=320)}

if __name__ == '__main__':
    app.run_server(debug=False)
