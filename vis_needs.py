import pandas as pd
import numpy as np
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# df = pd.read_csv(r'C:\Users\eoinv\Downloads\plenti\needs.csv')#
# df = df.fillna(' ')

needs_dict = {'CONNECTION': ['acceptance', 'affection', 'appreciation', 'belonging', 'cooperation', 'communication', 'closeness', 'community', 'companionship', 'compassion', 'consideration', 'consistency', 'empathy', 'inclusion', 'intimacy', 'love', 'mutuality', 'nurturing', 'respect/self-respect', 'safety', 'security', 'stability', 'support', 'to know and be known', 'to see and be seen', 'to understand and', 'be understood', 'trust', 'warmth'],
'PHYSICAL WELL-BEING': ['air', 'food', 'movement/exercise', 'rest/sleep', 'sexual expression', 'safety', 'shelter', 'touch', 'water', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
'HONESTY': ['authenticity', 'integrity', 'presence', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
'PLAY': ['joy', 'humor', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
'PEACE': ['beauty', 'communion', 'ease', 'equality', 'harmony', 'inspiration', 'order', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
'AUTONOMY': ['choice', 'freedom', 'independence', 'space', 'spontaneity', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
'MEANING': ['awareness', 'celebration of life', 'challenge', 'clarity', 'competence', 'consciousness', 'contribution', 'creativity', 'discovery', 'efficacy', 'effectiveness', 'growth', 'hope', 'learning', 'mourning', 'participation', 'purpose', 'self-expression', 'stimulation', 'to matter', 'understanding', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']}
df = pd.DataFrame.from_dict(needs_dict)

def display_col(df, listy):
    for col in df.columns:
        st.title(col)
        st.session_state.checkbox_clicked = False
        select = st.checkbox(f'I value {col}')#, key=f'{random.randrange(1, 10**3):03}')#, key=random.randrange(111111, 999999, 6))
        select_alt = st.checkbox(f'Something more specific related to {col} (you can select more than one)?')#, key=f'{random.randrange(1, 10**3):03}')#, key=random.randrange(111111, 999999, 6))
        
        if select_alt:

            st.session_state.checkbox_clicked = True

        check_selection(select, select_alt, col, listy)

def check_selection(select, select_alt, col, listy):
    if select == False and st.session_state.checkbox_clicked == True:

        add_to_list({'select_alt':True}, select, select_alt, col, listy)
    if select == True and st.session_state.checkbox_clicked == False: 

        add_to_list({'select':True}, select, select_alt, col, listy)
    if select == True and st.session_state.checkbox_clicked == True: 

        add_to_list({'select':True, 'select_alt':True}, select, select_alt, col, listy)

def add_to_list(selection:dict, select, select_alt, col, listy):
    if 'select_alt' in selection.keys():
        if len(selection) == 1 and selection['select_alt'] == True:

            display_col_contents(df, col, listy)
        if len(selection) == 2 and selection['select_alt']==True:

            listy.append(col)
            display_col_contents(df, col, listy)
    if 'select' in selection.keys():
        if len(selection) == 1 and selection['select']==True:

            listy.append(col)



def display_col_contents(df, col, listy):
    options = []
    for item in df[col]:
        if item != df["physical well-being"].iloc[-1]:

            options.append(item)


    #newfunction?
    values = st.multiselect('I value:', options=options)
    listy += values



if "checkbox_clicked" not in st.session_state:    
    st.session_state.checkbox_clicked = False


listy = []
df.columns = [col.lower() for col in df.columns]
display_col(df, listy)

if 'physical well-being' in listy:
    index_list = listy.index('physical well-being')
    listy = listy[:index_list]+['wellbeing']+listy[index_list+1:]

final_string = ', '.join(i for i in listy)
#final_string = final_string[1:]
st.header(f'I value: {final_string}')



if len(listy) > 0:
    wordcloud = WordCloud().generate(final_string)


    # Display the generated image:
    fig, ax = plt.subplots(figsize = (12, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(fig)