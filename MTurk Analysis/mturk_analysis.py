import pandas as pd
import ast

def get_iou(bb1, bb2):
    """
    Reference: https://stackoverflow.com/questions/25349178/...
    ...calculating-percentage-of-bounding-box-overlap-for-image-detector-evaluation
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters
    ----------
    bb1 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x, y) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner

    Returns
    -------
    float
        in [0, 1]
    """
    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou

keydf = pd.read_excel('Key.xlsx')
batchdf = pd.read_csv('Final_MTurk_Raw.csv')
mergedf = batchdf.merge(keydf, left_on='Input.image_url', right_on='Mturk_URL', how='outer')
mergedf = mergedf[['WorkerId','ImageNo','AssignmentStatus','WorkTimeInSeconds','Reward','Answer.annotation_data','Mturk_URL','Description_y','RefL','RefT','RefW','RefH','LaptopPerformance']]
mergedf = mergedf.rename(columns={"Description_y": "Description"})
mergedf['Left'] = 0
mergedf['Top'] = 0
mergedf['Width'] = 0
mergedf['Height'] = 0
mergedf['IOU'] = 0
mergedf['Hit'] = 0
for i in range(mergedf.shape[0]):
    currStr = mergedf['Answer.annotation_data'][i]
    currStr = currStr[1:len(currStr)-1]
    currDict = ast.literal_eval(currStr)
    mergedf.loc[i,'Left'] = currDict['left']
    mergedf.loc[i,'Top'] = currDict['top']
    mergedf.loc[i,'Width'] = currDict['width']
    mergedf.loc[i,'Height'] = currDict['height']
    b1tmp = {'x1': mergedf.loc[i,'Left'], 'x2': mergedf.loc[i,'Left']+mergedf.loc[i,'Width'],
             'y1': mergedf.loc[i,'Top'],'y2': mergedf.loc[i,'Top']+mergedf.loc[i,'Height']}
    b2tmp = {'x1': mergedf.loc[i, 'RefL'], 'x2': mergedf.loc[i, 'RefL'] + mergedf.loc[i, 'RefW'],
             'y1': mergedf.loc[i, 'RefT'], 'y2': mergedf.loc[i, 'RefT'] + mergedf.loc[i, 'RefH']}
    mergedf.loc[i,'IOU'] = get_iou(b1tmp, b2tmp)
    mergedf.loc[i, 'Hit'] = 1 if mergedf.loc[i,'IOU']>0.3 else 0
mergedf = mergedf.drop(columns='Answer.annotation_data')
writer = pd.ExcelWriter('output.xlsx')
mergedf.to_excel(writer,'Sheet1')
writer.save()