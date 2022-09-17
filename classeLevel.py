from turtle import speed
import pygame
import config
from classeTile import Tile
from classePlayer import Player

class Level:
    def __init__(self, level_map, surface):
        # Superfície onde o nível será desenhado
        self.display_surface = surface

        # Jogador
        self.player = pygame.sprite.GroupSingle()

        # Agrupa todas as superfícies do nível atual geradas por generate_level()
        self.level_tiles = pygame.sprite.Group() 
        self.generate_level(level_map)

        
    def generate_level(self, level_map_matrix): # Gera o mapa baseado no nível (baseado no argumento level_map recebido na construtora)
        tile_size = config.level_tile_size

        for row_index, row in enumerate(level_map_matrix):
            for column_index, tile in enumerate(row):
                x = column_index * tile_size # Gera a posição x do tile
                y = row_index * tile_size # Gera a posição y do tile
                
                if tile == 'X':
                    tile = Tile((x, y), tile_size) # Invoca a classe Tile que cria o sprite daquele bloco
                    self.level_tiles.add(tile) # Adiciona o tile criado no atributo que agrupa os tiles
                
                if tile == 'P':
                    # Os valores de posição são ajustados pois o player é gerado com base nas coordenadas em seu midbottom
                    player_origin_x = x + (tile_size/2)
                    player_origin_y = y + (tile_size)

                    # Gera o jogador usando a classe Player e enviando a posição inicial
                    player_sprite = Player((player_origin_x, player_origin_y)) 
                    self.player.add(player_sprite)

    def horizontal_player_collision(self):
        ...

    def vertical_player_collision(self, player):
        for tile in self.level_tiles:
            if tile.rect.colliderect(player):
                if player.speed.y > 0: # Se o jogador estiver caindo
                    player.speed.y = 0
                    player.set_jumping_status(False)
                    player.set_on_ground_status(True)
                    player.rect.bottom = tile.rect.top
                
                elif player.speed.y < 0: # Se o jogador estiver subindo
                    player.speed.y = 0
                    player.rect.top = tile.rect.bottom




    def run(self, event_listener):
        player = self.player.sprite

        player.update(event_listener)
        self.vertical_player_collision(player)
        
        
        #player.reposition()
        #self.horizontal_player_collision()
        #self.player.sprite.apply_speed()

        # Draw
        self.player.draw(self.display_surface)
        self.level_tiles.draw(self.display_surface)