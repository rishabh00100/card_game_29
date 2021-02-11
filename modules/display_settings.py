

fontScale = 1
color = (235,227,170)
thickness = 1
text_buffer = 18
console_size = 250

def get_deck_coords(back_width, back_height, deck_size, card_width, card_height):
    deck_coords = { "Player_1": {"deck": {  "start_point": (int((back_width-deck_size[0])/2), back_height-50-deck_size[1]), 
                                                        "end_point":(int((back_width+deck_size[0])/2), back_height-50)},
                                "cards": {  "valid_card": 50,
                                            "invalid_card": 70,
                                            "played_card": (int(back_width/2-card_width/2), int(back_height/2+card_height/10))},
                                "console": {"start_point": (int((back_width+deck_size[0])/2), back_height-50-console_size),
                                            "end_point": (int((back_width+deck_size[0])/2)+350, back_height-50),
                                            "player_name": (int((back_width+deck_size[0])/2)+text_buffer, back_height-50-console_size+40),
                                            "current_bid": (int((back_width+deck_size[0])/2)+text_buffer, back_height-50-console_size+80),
                                            "current_score": (int((back_width+deck_size[0])/2)+text_buffer, back_height-50-console_size+120),
                                            "current_gp": (int((back_width+deck_size[0])/2)+text_buffer, back_height-50-console_size+160),
                                            "score_to_win": (int((back_width+deck_size[0])/2)+text_buffer, back_height-50-console_size+200)}
                                },
                    "Player_2": {"deck": {  "start_point": (50, int((back_height-deck_size[0])/2)), 
                                            "end_point":(50+deck_size[1], int((back_height+deck_size[0])/2))},
                                "cards": {  "valid_card": 70,
                                            "invalid_card": 50,
                                            "played_card": (int(back_width/2-card_height*1.1), int(back_height/2-card_width/2))},
                                "console": {"start_point": (50, int((back_height+deck_size[0])/2)),
                                            "end_point": (50+deck_size[1], int((back_height+deck_size[0])/2)+console_size),
                                            "player_name": (50+text_buffer, int((back_height+deck_size[0])/2)+40),
                                            "current_bid": (50+text_buffer, int((back_height+deck_size[0])/2)+80),
                                            "current_score": (50+text_buffer, int((back_height+deck_size[0])/2)+120),
                                            "current_gp": (50+text_buffer, int((back_height+deck_size[0])/2)+160),
                                            "score_to_win": (50+text_buffer, int((back_height+deck_size[0])/2)+200)}
                                },
                    "Player_3": {"deck": {  "start_point": (int((back_width-deck_size[0])/2), 50), 
                                            "end_point":(int((back_width+deck_size[0])/2), 50+deck_size[1])},
                                "cards": {  "valid_card": 70,
                                            "invalid_card": 50,
                                            "played_card": (int(back_width/2-card_width/2), int(back_height/2-card_height*1.1))},
                                "console": {"start_point": (int((back_width-deck_size[0])/2)-350, 50),
                                            "end_point": (int((back_width-deck_size[0])/2), 50+console_size),
                                            "player_name": (int((back_width-deck_size[0])/2)-350+text_buffer, 50+40),
                                            "current_bid": (int((back_width-deck_size[0])/2)-350+text_buffer, 50+80),
                                            "current_score": (int((back_width-deck_size[0])/2)-350+text_buffer, 50+120),
                                            "current_gp": (int((back_width-deck_size[0])/2)-350+text_buffer, 50+160),
                                            "score_to_win": (int((back_width-deck_size[0])/2)-350+text_buffer, 50+200)}
                                },
                    "Player_4": {"deck": {  "start_point": (back_width-50-deck_size[1], int((back_height-deck_size[0])/2)), 
                                            "end_point":(back_width-50, int((back_height+deck_size[0])/2))},
                                "cards": {  "valid_card": 50,
                                            "invalid_card": 70,
                                            "played_card": (int(back_width/2+card_height/10), int(back_height/2-card_width/2))},
                                "console": {"start_point": (back_width-50-deck_size[1], int((back_height-deck_size[0])/2)-console_size), 
                                            "end_point": (back_width-50, int((back_height-deck_size[0])/2)),
                                            "player_name": (back_width-50-deck_size[1]+text_buffer, int((back_height-deck_size[0])/2)-console_size+40),
                                            "current_bid": (back_width-50-deck_size[1]+text_buffer, int((back_height-deck_size[0])/2)-console_size+80),
                                            "current_score": (back_width-50-deck_size[1]+text_buffer, int((back_height-deck_size[0])/2)-console_size+120),
                                            "current_gp": (back_width-50-deck_size[1]+text_buffer, int((back_height-deck_size[0])/2)-console_size+160),
                                            "score_to_win": (back_width-50-deck_size[1]+text_buffer, int((back_height-deck_size[0])/2)-console_size+200)}
                                },
                    "Game_Console": {"title_start_point": (20, back_height+40),
                                    "heading_start_point": (20, back_height+80),
                                    "subheading_start_point": (20, back_height+120),
                                    "action_start_point": (20, back_height+160),
                                    "action2_start_point": (20, back_height+200)}
                    }
    return deck_coords



