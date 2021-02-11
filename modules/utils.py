import os, sys, time
import cv2
import copy
from modules.display_settings import *
font = cv2.FONT_HERSHEY_SIMPLEX 


class cv2_display:
    def __init__(self, player_list, round_number):
        self.reset_background_img()
        self.round_number = round_number
        self.player_list = player_list
        self.none_card = cv2.imread(os.path.join(os.getcwd(), "modules/img/back-side.png"))
        self.none_card = cv2.resize(self.none_card, (160,232))
        self.card_height, self.card_width, _ = self.none_card.shape
        self.deck_size = self.get_deck_size()
        self.deck_coords = get_deck_coords(self.back_width, self.back_height, self.deck_size, self.card_width, self.card_height)
        self.set_player_decks()
        self.update_player_console()

    def get_deck_size(self, buffer=50):
        deck_width = 2*buffer + self.card_width + int(self.card_width/4)*7
        deck_height = 2*buffer + self.card_height + 20
        return (deck_width, deck_height)

    def reset_background_img(self, GC_Flag=True):
        if GC_Flag:
            # Start a new background
            self.displ_img = cv2.imread(os.path.join(os.getcwd(), "modules/img/green_background.jpg"))
            self.displ_img = cv2.resize(self.displ_img, (0,0), fx=1.2, fy=1.8) 
            self.displ_height, self.back_width, _ = self.displ_img.shape
            self.back_height = int(0.8 * self.displ_height)
            self.game_console_height = self.displ_height - self.back_height
        # cv2.rectangle(self.displ_img, (0,self.back_height), (self.back_width, self.displ_height), (0, 0, 0), -1) # Game console
        cv2.rectangle(self.displ_img, (0,0), (self.back_width, self.back_height), (170, 227, 235), -1)

    def show_img(self, keyFlag=False, allowed_inputs=None):
        if keyFlag==True:
            print("keyFlag True")
            cv2.imshow('image', self.displ_img)
            if allowed_inputs is None:
                # Press any key situation
                if cv2.waitKey(0):
                    cv2.destroyAllWindows()
            else:
                if len(allowed_inputs) == 1:
                    # Default move available, choose it
                    cv2.destroyAllWindows()
                    return allowed_inputs[0]
                else:
                    # Press specific key situation
                    while True:
                        pressedKey = cv2.waitKey(33) & 0xFF
                        for each_allow_inp in allowed_inputs:
                            if pressedKey == ord(str(each_allow_inp)):
                                cv2.destroyAllWindows()
                                print("Keystroke received: ", pressedKey, chr(pressedKey))
                                return chr(pressedKey)
        else:
            # No Key press required
            print("keyFlag False")
            cv2.imshow('image', self.displ_img)
            # if cv2.waitKey(0):
            #     cv2.destroyAllWindows()
            cv2.destroyAllWindows()
            return None

    def update_game_console(self, stage_name=None, heading=None, sub_heading=None, action_line=None, action_line_2=None, allowed_inputs=None, show_img=False):
        cv2.rectangle(self.displ_img, (0,self.back_height), (self.back_width, self.displ_height), (0, 0, 0), -1)

        cv2.putText(self.displ_img, "Card Game 29 | {}".format(stage_name), self.deck_coords["Game_Console"]["title_start_point"], font, fontScale, (170,227,235), 3, cv2.LINE_AA)
        cv2.putText(self.displ_img, heading, self.deck_coords["Game_Console"]["heading_start_point"], font, fontScale, (170,227,235), 2, cv2.LINE_AA) 
        cv2.putText(self.displ_img, sub_heading, self.deck_coords["Game_Console"]["subheading_start_point"], font, fontScale, (170,227,235), 1, cv2.LINE_AA) 
        cv2.putText(self.displ_img, action_line, self.deck_coords["Game_Console"]["action_start_point"], font, fontScale, (255,255,255), 3, cv2.LINE_AA) 
        cv2.putText(self.displ_img, action_line_2, self.deck_coords["Game_Console"]["action2_start_point"], font, fontScale, (255,255,255), 3, cv2.LINE_AA) 
        # if show_img==True:
        player_input = self.show_img(show_img, allowed_inputs=allowed_inputs)
        return player_input

    def update_player_console(self):
        for player in self.player_list:
            player_name = player.name
            player_bid = ["Pass" if player.bidpass else player.bid][0]
            cv2.rectangle(self.displ_img, self.deck_coords[player_name]["console"]["start_point"], self.deck_coords[player_name]["console"]["end_point"], (93,65,87), -1)
            # Write info on console
            cv2.putText(self.displ_img, "{} | {}".format(player_name, player.team), self.deck_coords[player_name]["console"]["player_name"], font, fontScale, (170,227,235), 2, cv2.LINE_AA) 
            cv2.putText(self.displ_img, "Current Bid:   {}".format(player_bid), self.deck_coords[player_name]["console"]["current_bid"], font, fontScale, (170,227,235), thickness, cv2.LINE_AA)
            cv2.putText(self.displ_img, "Current Score: {}".format(player.score), self.deck_coords[player_name]["console"]["current_score"], font, fontScale, (170,227,235), thickness, cv2.LINE_AA)
            cv2.putText(self.displ_img, "Current GP:    {}".format(player.team.game_points), self.deck_coords[player_name]["console"]["current_gp"], font, fontScale, (170,227,235), thickness, cv2.LINE_AA)
            cv2.putText(self.displ_img, "Score to Win:  {}".format(player.team.req_match_score), self.deck_coords[player_name]["console"]["score_to_win"], font, fontScale, (170,227,235), thickness, cv2.LINE_AA)

    def set_player_decks(self, player_name=None):
        if not player_name:
            for player in self.player_list:
                player_name = player.name
                cv2.rectangle(self.displ_img, self.deck_coords[player_name]["deck"]["start_point"], self.deck_coords[player_name]["deck"]["end_point"], (186, 202, 168), -1)
        else:
            cv2.rectangle(self.displ_img, self.deck_coords[player_name]["deck"]["start_point"], self.deck_coords[player_name]["deck"]["end_point"], (186, 202, 168), -1)

    def show_cards(self, player_name, player_hand):
        player_hand_cp = copy.deepcopy(player_hand)
        if len(player_hand_cp) < 8:
            player_hand_cp.extend([None for i in range(8-len(player_hand_cp))])
        
        if player_name in ["Player_1", "Player_3"]:
            start_point_x = 50 + self.deck_coords[player_name]["deck"]["start_point"][0]
            for i, card in enumerate(player_hand_cp):
                start_point_y = self.deck_coords[player_name]["cards"]["invalid_card"] + self.deck_coords[player_name]["deck"]["start_point"][1]
                if not card:
                    # Card is None. Display rev_card
                    card_img = self.none_card
                else:
                    if card.validity == 1:
                        start_point_y = self.deck_coords[player_name]["cards"]["valid_card"] + self.deck_coords[player_name]["deck"]["start_point"][1]
                    card_img = card.card_img
                self.displ_img[start_point_y:start_point_y+self.card_height, start_point_x:start_point_x+self.card_width] = card_img
                start_point_x = start_point_x + int(self.card_width/4)
        else:
            start_point_y = 50 + self.deck_coords[player_name]["deck"]["start_point"][1]
            for i, card in enumerate(player_hand_cp):
                start_point_x = self.deck_coords[player_name]["cards"]["invalid_card"] + self.deck_coords[player_name]["deck"]["start_point"][0]
                if not card:
                    # Card is None. Display rev_card
                    card_img = self.none_card
                    card_img = cv2.rotate(card_img, cv2.ROTATE_90_CLOCKWISE) 
                else:
                    if card.validity == 1:
                        start_point_x = self.deck_coords[player_name]["cards"]["valid_card"] + self.deck_coords[player_name]["deck"]["start_point"][0]
                    card_img = cv2.rotate(card.card_img, cv2.ROTATE_90_CLOCKWISE) 
                self.displ_img[start_point_y:start_point_y+self.card_width, start_point_x:start_point_x+self.card_height] = card_img
                start_point_y = start_point_y + int(self.card_width/4)
        

    def display_game_state(self, player_list, cardsInATurn=None, playStage=False):
        print(">>display_game_state<<")
        self.reset_background_img(GC_Flag=False)
        self.set_player_decks()
        for each_player in player_list:
            self.show_cards(each_player.name, each_player.hand)
            self.update_player_console()
        if playStage:
            for player, card in cardsInATurn.items():
                player_name = player.name
                start_point_x, start_point_y = self.deck_coords[player_name]["cards"]["played_card"]
                if player_name in ["Player_1", "Player_3"]:
                    self.displ_img[start_point_y:start_point_y+self.card_height, start_point_x:start_point_x+self.card_width] = card.card_img
                else:
                    card_img = cv2.rotate(card.card_img, cv2.ROTATE_90_CLOCKWISE)
                    self.displ_img[start_point_y:start_point_y+self.card_width, start_point_x:start_point_x+self.card_height] = card_img

        player_input = self.show_img()

    def show_updated_hands(self, player):
        print(">>show_updated_hands<<")
        self.set_player_decks(player.name)
        self.show_cards(player.name, player.hand)
        player_input = self.show_img()



