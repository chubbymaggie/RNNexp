import numpy as np
from maneuver_prediction_rnn import evaluate
import sys
import neuralmodels.predictions
import pickle
import os

# Evaluates with various checkpoints and output thresholds to determine
# most optimal prediction parameters
if __name__ == '__main__':
    # Configure these
    checkpoints_params = np.append(np.arange(300, 599, 50), 599)
    thresh_params = np.arange(.6, .9, .01)

    save_file = sys.argv[1]
    maneuver_type = sys.argv[2]
    idx = sys.argv[3]

    folds = ['fold_1', 'fold_2', 'fold_3', 'fold_4', 'fold_5']
    cur_best_eval = {}

    for fold in folds:
        f1_score_best = 0
        for th in thresh_params:
            for cp in checkpoints_params:
                print '*******%s*********' % fold
                print 'Using thresh: %f and checkpoint: %s' % (th, cp)

                with open('settings.py','w') as f:
                    f.write('OUTPUT_THRESH = %f \n' % th)
                import neuralmodels.predictions

                [conMat, p_mat, re_mat, time_mat] = evaluate(
                    idx, fold, cp, 'multipleRNNs', maneuver_type)

                precision = np.mean(np.diag(p_mat)[1:])
                recall = np.mean(np.diag(re_mat)[1:])
                f1_score = (2*precision*recall)/(precision+recall)

                print('Precision: %s, recall: %s, '
                      'f1-score: %s \n' % (precision, recall, f1_score))

                if f1_score > f1_score_best:
                    f1_score_best = f1_score
                    cur_best_eval[fold] = {
                        'threshold': th, 'checkpoint': cp,
                        'precision': precision, 'recall': recall,
                        'f1-score': f1_score}
                    print('Storing best eval params for '
                          '%s so far: %s \n' % (fold, cur_best_eval[fold]))

    pickle.dump(cur_best_eval, open(save_file, 'wb'))