import cPickle as pickle
import sys
import numpy as np
import pandas as pd
import json

from preprocess_text_el import clean_text_basic

def open_pkl_and_vocab(model_name):
    ''' Load pickled model and list of words '''
    with open('/data/models/'+model_name+'.pkl', 'r') as f:
        model = pickle.load(f)

    with open('/data/el_keywords.pkl', 'r') as fp:
        vocab = pickle.load(fp)

    return model, vocab

def write_img_caption(model, indices_word, id, img_num, img_folder, df):

    img_arr = np.load('/data/'+img_folder+id+'_'+img_num+'.npy')
    preds = model.predict(img_arr, verbose=0)[0]

    print 'Recipe Number: ' + id

    generated = ''
    print '----- Generating with Img: ' + img_num
    sys.stdout.write(generated)

    pred_index = np.where(preds > .5)[0]

    for i, next_index in enumerate(pred_index):

        next_word = vocab[next_index]

        if generated == '':
            generated += next_word
            sys.stdout.write(next_word)
        else:
            generated += ', '+next_word
            sys.stdout.write(', ')
            sys.stdout.write(next_word)

        sys.stdout.flush()

    print '\n'

    id_int = int(id)
    true_y = df.query('id == @id_int')
    print 'The dish is called {}'.format(true_y['item_name'].values)
    print 'These are the true ingredients: '
    for item in true_y['ingred_list']:
        print item

    return preds


if __name__ == '__main__':
    df = pd.read_csv('/data/recipe_data.csv')

    model, vocab = open_pkl_and_vocab('VGG_sigmoid_el')
    pred_words = write_img_caption(model, vocab, '8452', '4', 'vgg_imgs/', df)
