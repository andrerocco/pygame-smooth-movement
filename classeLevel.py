from turtle import position, speed
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
    
    def handle_player_collision(self, player, delta_speed):
        dx, dy = delta_speed

        for tile in self.level_tiles.sprites():
            # Colisão horizontal
            if tile.rect.colliderect(player.rect.x + dx, player.rect.y, player.rect.width, player.rect.height): # Testa a colisão do deslocamento horizontal
                if player.speed.x < 0: # Caso o jogador colida com um superfície pela esquerda
                    dx = tile.rect.right - player.rect.left
                elif player.speed.x > 0: # Caso o jogador colida com um superfície pela direita
                    dx = tile.rect.left - player.rect.right
                else:
                    dx = 0

            # Colisão vertical
            if tile.rect.colliderect(player.rect.x, player.rect.y + dy, player.rect.width, player.rect.height): # Testa a colisão do deslocamento vertical
                if player.speed.y < 0 and (tile.rect.bottom <= player.rect.top): # Jogador "subindo"
                    dy = (tile.rect.bottom - player.rect.top)
                    player.speed.y = 0 # Reinicia a gravidade
                if player.speed.y > 0 and (tile.rect.top >= player.rect.bottom): # Jogador "caindo"
                    dy = (tile.rect.top - player.rect.bottom)
                    player.speed.y = 0 # Reinicia a gravidade  
                    player.set_jumping_status(False)
                    player.set_on_ground_status(True)
                else:
                    dy = 0

        return (dx, dy) 


    def run(self, event_listener):
        player = self.player.sprite

        # A variável delta_speed é uma tupla com os valores de deslocamento calculados baseados no player
        delta_speed = player.calculate_speed(event_listener)
        
        # A variável collided_delta_speed é uma tupla com os valores de deslocamento transformados a partir das colisões
        collided_delta_speed = self.handle_player_collision(player, delta_speed)
        
        # Aplica o deslocamento final no jogador
        player.update(collided_delta_speed)

        # Draw
        self.player.draw(self.display_surface)
        self.level_tiles.draw(self.display_surface)