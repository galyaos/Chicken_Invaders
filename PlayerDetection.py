# Description: This file contains the player detection logic.

def detect_players(image, segmenter, mode="double"):
    num_bodies = 2 if mode == "double" else 1  # Limit detected bodies based on mode
    body_bboxes = segmenter.segment_foreground(image, num_bodies)

    if not body_bboxes and segmenter.last_bboxes:
        body_bboxes = segmenter.last_bboxes

    # Limit number of players
    body_bboxes = body_bboxes[:num_bodies]

    # Sort players based on their x-coordinate (bx) to assign player 0 and player 1
    body_bboxes.sort(key=lambda bbox: bbox[0])  # Sort by bx (leftmost first)

    players = []
    for i, body in enumerate(body_bboxes):
        bx, by, bw, bh = body
        players.append({'id': i, 'body': (bx, by, bw, bh)})

    return players
