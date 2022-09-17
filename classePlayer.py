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
        self.max_walking_speed = 4

        # Acelerações
        self.gravity = 0.5
        self.acceleration = pygame.Vector2(0, self.gravity)
        self.input_strength = 0.6 # Altera a força do input do jogador
        self.friction = 0.75 # Desaceleração do jogador em porcentagem
        self.knockback_strength = 20 # Altera a força do knockback
        self.jump_strength = 8 # Altera a força do pulo

        # Atributos de input
        self.thrust = 0

        # Atributos de estado
        self.jumping_status = False
        self.on_ground_status = True
        self.facing_right_status = True


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
        
        self.acceleration.x += (self.input_strength * self.thrust)

        # Movimento vertical
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.jumping_status is False:
            self.jump()

    def apply_accceleration(self):
        self.walking_speed += self.acceleration.x
        self.acceleration.x = 0

        if self.walking_speed > self.max_walking_speed: # Se a velocidade for maior que a velocidade máxima
            self.walking_speed = self.max_walking_speed
        elif self.walking_speed < -self.max_walking_speed: # Se a velocidade for menor que o valor negativo da velocidade máxima
            self.walking_speed = -self.max_walking_speed

    def apply_friction(self):
        if self.thrust == 0: # Se o jogador não estiver pressionando esquerda ou direita aplica a frição na valocidade da caminhada
            self.walking_speed = int(self.walking_speed * self.friction * 1000)/1000 # Arredonda para 4 pontos de precisão

        # Aplica a fricção na velocidade do knockback
        if self.on_ground_status is True: # Caso o jogador estiver no ar (menos resistência)
            self.knockback_speed.x = int(self.knockback_speed.x * 0.97 * 1000)/1000 # Arredonda para 4 pontos de precisão


    def knockback(self, target_position):
        self.on_ground_status = False

        # Calcula a direção do knockback
        direction = pygame.Vector2(target_position) - pygame.Vector2(self.rect.center)
        print(direction)
        direction = direction.normalize()
        print(direction)

        # Aplica o knockback
        self.knockback_speed = -(direction * self.knockback_strength)


    def calculate_speed(self, event_listener):
        # Se o jogador atirar uma flecha e tiver flechas disponíveis
        for event in event_listener:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.knockback(pygame.mouse.get_pos())
                self.speed.y += self.knockback_speed.y
        
        # Aplica a aceleração do input
        self.movement_input() # Muda os valores de aceleração
        self.apply_accceleration() # Aplica a aceleração ao vetor de velocidade

        # Aplica a fricção nos movimentos horizontais
        self.apply_friction()



    def update(self, event_listener): # Calcula o movimento baseado nos inputs
        self.calculate_speed(event_listener)
        self.move()


    def move(self):
        # Movimento x
        self.speed.x = self.walking_speed + self.knockback_speed.x # A velocidade resultante é a soma da velocidade de caminhada e da velocidade de knockback
        self.precise_rect_position_x += self.speed.x # A posição precisa será float
        self.rect.x = int(self.precise_rect_position_x) # A posição recebida pelo retângulo precisa ser inteira para posicionar o pixel

        # Movimento y
        self.speed.y += self.gravity # Aplica a aceleração da gravidade
        self.rect.y += self.speed.y



    # Setters
    def set_on_ground_status(self, status: bool):
        self.on_ground_status = status
    def set_jumping_status(self, status: bool):
        self.jumping_status = status