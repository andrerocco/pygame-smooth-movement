import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        # Atributos padrões
        self.image = pygame.Surface((20,40))
        self.image.fill('red')
        self.rect = self.image.get_rect(midbottom=position)

        # Mudanças de posição
        self.precise_rect_position_x = self.rect.x
        
        # Velocidades
        self.speed = pygame.Vector2(0, 0)

        self.knockback_speed = pygame.Vector2(0, 0)
        self.walking_speed = 0
        self.max_walking_speed = 5

        # Acelerações
        self.gravity = 0.5
        self.acceleration = pygame.Vector2(0, self.gravity)
        self.input_strength = 0.6 # Altera a força do input do jogador
        self.ground_friction = 0.75 # Desaceleração do chão em porcentagem
        self.air_friction = 0.98 # Desaceleração do ar em porcentagem
        self.knockback_strength = 13 # Altera a força do knockback
        self.jump_strength = 8 # Altera a força do pulo

        # Atributos de input
        self.thrust = 0

        # Atributos de estado
        self.jumping_status = False
        self.on_ground_status = True
        self.facing_right_status = True
        self.contador = 0


    def jump(self):
        self.speed.y = -self.jump_strength
        self.jumping_status = True
        self.on_ground_status = False

    def movement_input(self):
        keys = pygame.key.get_pressed()

        # Movimento horizontal
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.thrust = 1
            self.facing_right_status = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.thrust = -1
            self.facing_right_status = False
        
        # Se o jogador não estiver pressionando esquerda ou direita
        if not (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.thrust = 0

        self.acceleration.x = (self.input_strength * self.thrust)

        # Movimento vertical
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.jumping_status is False:
            self.jump()

    def apply_accceleration(self):
        temp_speed_result = self.speed.x + self.acceleration.x

        # Se a velocidade for maior que a máxima de caminhada e o jogador estiver pressionando a tecla de movimento na mesma direção, não entra na condição
        if not (temp_speed_result > self.max_walking_speed and self.thrust == 1) and not (temp_speed_result < -self.max_walking_speed and self.thrust == -1):
            self.speed.x += self.acceleration.x
        
        # Aplica a aceleração da gravidade
        self.speed.y += self.acceleration.y

    def apply_friction(self):
        #print("Acceleration: ", self.acceleration.x)
        #print("Speed: {} - Max speed: {}".format(self.speed.x, self.max_walking_speed))
        if self.on_ground_status and self.thrust == 0:
            self.speed.x = int(self.speed.x * self.ground_friction * 1000)/1000 # Arredonda para 4 pontos de precisão
        elif self.on_ground_status and abs(self.speed.x) > self.max_walking_speed:
            self.speed.x = int(self.speed.x * self.ground_friction * 1000)/1000 # Arredonda para 4 pontos de precisão

        if not self.on_ground_status:
            self.speed.x = int(self.speed.x * self.air_friction * 1000)/1000 # Arredonda para 4 pontos de precisão


    def knockback(self, target_position):
        self.on_ground_status = False

        # Calcula a direção do knockback
        direction = pygame.Vector2(target_position) - pygame.Vector2(self.rect.center)
        direction = direction.normalize()

        # Aplica o knockback
        self.speed = -(direction * self.knockback_strength)


    def calculate_speed(self, event_listener):
        # Se o jogador atirar uma flecha e tiver flechas disponíveis
        for event in event_listener:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.knockback(pygame.mouse.get_pos())

        self.contador += 1
        if self.contador == 10:
            print(self.speed.x)
            self.contador = 0

        # Aplica a aceleração do input
        self.movement_input() # Muda os valores de aceleração
        self.apply_accceleration() # Aplica a aceleração ao vetor de velocidade

        # Aplica a fricção na aceleração horizontal
        self.apply_friction()



    def update(self, event_listener): # Calcula o movimento baseado nos inputs
        self.calculate_speed(event_listener)
        self.move()


    def move(self):
        # Movimento x
        self.precise_rect_position_x += self.speed.x # A posição precisa será float
        self.rect.x = int(self.precise_rect_position_x) # A posição recebida pelo retângulo precisa ser inteira para posicionar o pixel

        # Movimento y
        self.rect.y += self.speed.y



    # Setters
    def set_on_ground_status(self, status: bool):
        self.on_ground_status = status
    def set_jumping_status(self, status: bool):
        self.jumping_status = status