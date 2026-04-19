# Diagramas del Proyecto

## Diagrama de Clases

```mermaid
classDiagram
    %% ENTIDADES
    class Entidad {
        <<abstract>>
        -_hp_max: int
        -_hp_actual: int
        -_ataque: int
        -_defensa: int
        -_sprite: Optional~Sprite~
        +hp_max: int
        +hp_actual: int
        +ataque: int
        +defensa: int
        +ataque_total: int
        +defensa_total: int
        +sprite: Optional~Sprite~
        +esta_vivo()* bool
        +recibir_daño(daño: int) None
        +curar(cantidad: int) None
        +tiene_sprite() bool
        +puede_recibir_daño()* bool
        +puede_ser_destruido()* bool
    }

    class Personaje {
        -_nombre: str
        -_nivel: int
        -_experiencia: int
        -_experiencia_siguiente_nivel: int
        -_oro: int
        -_inventario: list~Item~
        -_arma_equipada: Optional~Equipamiento~
        -_armadura_equipada: Optional~Equipamiento~
        -_velocidad_disparo: float
        -_dano_proyectil: float
        -_velocidad_proyectil: float
        -_rebotes: int
        +nombre: str
        +nivel: int
        +experiencia: int
        +experiencia_siguiente_nivel: int
        +oro: int
        +inventario: list~Item~
        +arma_equipada: Optional~Equipamiento~
        +armadura_equipada: Optional~Equipamiento~
        +ataque_total: int
        +defensa_total: int
        +cooldown_disparo: float
        +esta_vivo() bool
        +ganar_experiencia(xp: int) None
        -_subir_nivel() None
        +agregar_item(item: Item) None
        +usar_item(item: Item) bool
        +equipar(equipamiento: Equipamiento) None
        +agregar_oro(cantidad: int) None
        +quitar_oro(cantidad: int) None
        +mejorar_velocidad_disparo() None
        +mejorar_dano_proyectil() None
        +mejorar_velocidad_proyectil() None
        +mejorar_rebote() None
        +reiniciar_upgrades() None
    }

    class Enemigo {
        -_nombre: str
        -_tipo: Literal
        -_experiencia_al_derrotar: int
        -_oro_al_derrotar: int
        -_es_jefe: bool
        -_sprite: Optional~Sprite~
        -center_x: float
        -center_y: float
        +nombre: str
        +tipo: str
        +experiencia_al_derrotar: int
        +oro_al_derrotar: int
        +es_jefe: bool
        +sprite: Optional~Sprite~
        +esta_vivo() bool
        +tiene_sprite() bool
    }

    Entidad <|-- Personaje
    Entidad <|-- Enemigo

    %% PROYECTILES
    class Proyectil {
        -_direccion_x: float
        -_direccion_y: float
        -_dano: float
        -velocidad: float
        -es_del_jugador: bool
        -sprite: Sprite
        -activo: bool
        -_rebotes_maximos: int
        -_rebotes_actuales: int
        +esta_vivo() bool
        +puede_recibir_daño() bool
        +puede_ser_destruido() bool
        +actualizar() None
        +esta_fuera_de_pantalla() bool
        +tiene_sprite() bool
    }

    Entidad <|-- Proyectil

    %% ITEMS
    class Item {
        <<abstract>>
        -_nombre: str
        -_descripcion: str
        +nombre: str
        +descripcion: str
        +usar(personaje: Personaje)* bool
    }

    class Equipamiento {
        -_tipo: str
        -_bonus: int
        -_precio: int
        +tipo: str
        +bonus: int
        +precio: int
        +usar() bool
        +vender() int
    }

    class Consumible {
        -_efecto: int
        -_precio: int
        +efecto: int
        +precio: int
        +usar() bool
        +vender() int
    }

    class Tesoro {
        -_valor: int
        -_precio: int
        -center_x: float
        -center_y: float
        +valor: int
        +precio: int
        +usar() int
        +vender() int
    }

    class TrampaExplosiva {
        -_daño: int
        -_alcance: int
        +daño: int
        +alcance: int
        +usar() bool
        +activar() None
    }

    class ItemDrop {
        -_tipo: str
        -_valor: int
        -_tiempo_expiracion: float
        -_sprites: list
        +tipo: str
        +valor: int
        +expirado: bool
        +recoger() None
        +actualizar_tiempo() None
        +tiene_sprite() bool
        +crear_desde_enemigo() ItemDrop
    }

    class MejoraProyectil {
        -_tipo: str
        -_descripcion: str
        +usar(personaje: Personaje) bool
    }

    Item <|-- Equipamiento
    Item <|-- Consumible
    Item <|-- Tesoro
    Item <|-- TrampaExplosiva
    Item <|-- ItemDrop
    Item <|-- MejoraProyectil

    %% SERVICIOS
    class GestorProyectiles {
        -_ancho: int
        -_alto: int
        -proyectiles: list~Proyectil~
        -lista_sprites: list
        -_timers_disparo_enemigo: list
        -_cooldown_jugador: float
        +crear_proyectil_jugador() Proyectil
        +crear_proyectil_enemigo() Proyectil
        +actualizar_proyectiles(dt) None
        +verificar_colisiones_enemigos() None
        +eliminar_proyectil() None
        +eliminar_enemigo() None
        +limpiar() None
    }

    class GestorCombate {
        +_cooldown: float
        +verificar_combate(atacante, defensor) bool
        +actualizar_cooldown(dt) None
        +puede_combatir() bool
        +procesar_derrota_enemigo() None
    }

    class GestorItems {
        +verificar_colisiones() None
        +procesar_tesoro() None
        +procesar_trampa() None
    }

    class GestorAudio {
        -_instancia: GestorAudio$
        -_sonido_disparo: Sound
        -_sonido_recompensa: Sound
        -_sonido_victoria: Sound
        -_sonido_ui: Sound
        +obtener() GestorAudio$
        +reproducir_disparo()$ None
        +reproducir_recompensa()$ None
        +reproducir_victoria()$ None
        +reproducir_ui()$ None
    }

    %% SISTEMA DE TIENDA
    class ItemTienda {
        -item: Item
        -stock: int
        +nombre: str
        +precio: int
        +tipo: str
        +bonus: int
    }

    class SistemaTienda {
        +ITEMS_TIENDA: list~ItemTienda~$
        +getter_items_tienda()$ list~ItemTienda~
        +comprar_item(indice: int, personaje) tuple~bool, str~
        +vender_item(indice: int, personaje) tuple~bool, str~
    }

    %% MUNDO
    class Escenario {
        -_ancho: int
        -_alto: int
        -_areas: dict~str, Area~
        -_area_actual: str
        -_nivel: int
        +nivel: int
        +ancho: int
        +alto: int
        +area_actual: str
        +area: Area
        +enemigos: list
        +items: list
        +areas_disponibles: list~str~
        +cambiar_area(tipo: str) bool
        +ir_area_siguiente() bool
        +ir_area_anterior() bool
        +agregar_enemigo(enemigo) None
        +agregar_item(item) None
        +regenerar_contenido() None
    }

    class Area {
        -_tipo: str
        -_ancho: int
        -_alto: int
        -_nivel: int
        -_enemigos: list~Enemigo~
        -_items: list~Item~
        -_config: dict
        +TIPOS: dict$
        +tipo: str
        +nombre: str
        +descripcion: str
        +color_fondo: tuple
        +ancho: int
        +alto: int
        +enemigos: list~Enemigo~
        +items: list~Item~
        -_generar_contenido() None
        -_generar_enemigos(cantidad: int) None
        -_generar_items(cantidad: int) None
        +agregar_enemigo(enemigo: Enemigo) None
        +agregar_item(item: Item) None
    }

    Escenario o-- Area
    Area o-- Enemigo
    Area o-- Item

    %% UI
    class HUD {
        -_personaje: Personaje
        +dibujar() None
    }

    class MenuPausa {
        -_personaje: Personaje
        -_modo_actual: str
        +abierto: bool
        +abrir() None
        +cerrar() None
        +manejar_input(key) bool
        +dibujar() None
    }

    class MenuTienda {
        -_personaje: Personaje
        -_escenario: Escenario
        -_modo_actual: str
        -_mensaje: str
        +abierto: bool
        +abrir() None
        +cerrar() None
        +manejar_input() bool
        +dibujar() None
    }

    %% RELACIONES
    Personaje --> GestorCombate
    Personaje --> GestorItems
    Personaje --> HUD
    Personaje --> MenuPausa
    Personaje --> MenuTienda
    GestorProyectiles --> Proyectil
    GestorProyectiles --> Enemigo
    Enemigo ..> ItemDrop : drop
    MenuPausa ..> MenuTienda
    ItemTienda --> Equipamiento
    ItemTienda --> MejoraProyectil
    SistemaTienda ..> ItemTienda
    SistemaTienda ..> Personaje
```

## Descripción de las Relaciones

### Herencia (Generalización)

- **Entidad** → Clase abstracta base de la cual heredan `Personaje`, `Enemigo` y `Proyectil`. Define los atributos comunes: HP, ataque, defensa, sprite.
- **Item** → Clase abstracta base de la cual heredan `Equipamiento`, `Consumible`, `Tesoro`, `TrampaExplosiva`, `ItemDrop` y `MejoraProyectil`.

### Asociación

- **Personaje** ↔ **GestorCombate**: El personaje puede atacar y recibir ataques a través del gestor de combate.
- **Personaje** ↔ **GestorItems**: Gestiona la colección de items del suelo.
- **GestorProyectiles** ↔ **Proyectil**: Crea y gestiona proyectiles.
- **GestorProyectiles** ↔ **Enemigo**: Verifica colisiones projectile-enemigo.
- **ItemDrop** ↔ **Enemigo**: Los enemigos sueltan items al morir.
- **Escenario** ↔ **Area**: Un escenario contiene múltiples áreas.
- **Personaje** ↔ **MenuPausa**: El menú de pausa actúa sobre el personaje.
- **Personaje** ↔ **MenuTienda**: El menú de tienda actúa sobre el personaje.
- **GestorAudio** ↔ *(singleton)*: Proporciona métodos estáticos para reproducir sonidos del juego.
- **SistemaTienda** ↔ **Personaje**: Gestiona transacciones de compra/venta de items.
- **SistemaTienda** ↔ **ItemTienda**: Contiene items disponibles para la venta.

### Agregación

- **Personaje** → **Inventario** (list[Item]): El personaje tiene un inventario.
- **GestorProyectiles** → **Proyectiles** (list[Proyectil]): Gestor administra múltiples proyectiles.
- **Area** → **Enemigos** (list[Enemigo]): El área contiene enemigos.
- **Area** → **Items** (list[Item]): El área contiene items.
- **Escenario** → **Area** (contains): El escenario contiene múltiples áreas.

### Composición

- **Escenario** → **Area**: El escenario gestiona las áreas. Si el escenario se destruye, las áreas también.
- **GestorProyectiles** → **_timers_disparo_enemigo, _cooldown_jugador**: Timers internos del gestor.

## Notas de Diseño

1. **Patrón Service Layer**: `GestorProyectiles`, `GestorCombate`, `GestorItems` y `SistemaTienda` actúan como servicios que gestionan lógicas de juego específicas.
2. **Patrón Singleton**: `GestorAudio` implementa el patrón singleton para mantener una única instancia global de audio.
3. **Patrón Observer implícito**: El `HUD` observa al `Personaje` para actualizar la UI cuando cambian los stats.
4. **Patrón Factory implícito**: `GestorProyectiles.crear_proyectil_jugador()` y `GestorProyectiles.crear_proyectil_enemigo()` actúan como factories.
5. **Patrón Entity-Component**: Proyectil tiene su propio sprite, lo que permite rendering independiente.
6. **Encapsulamiento**: Uso de properties para proteger los atributos privados.
7. **Herencia vs Composición**: Se usa herencia para entidades del dominio (Personaje, Enemigo, Items, Proyectil) y composición para sistemas (Gestores).
8. **Sistema de Upgrades**: Personaje tiene métodos para mejorar estadísticas de proyectiles (velocidad, daño, rebotes).
9. **Sistema de Tienda**: `SistemaTienda` centraliza la lógica de compra/venta de items, interactuando con el inventario y oro del personaje.

## Atributos Nuevos en Personaje (Sistema de Proyectiles)

- **_velocidad_disparo**: Controla la velocidad de fuego del personaje.
- **_dano_proyectil**: Daño base de los proyectiles del personaje.
- **_velocidad_proyectil**: Velocidad de movimiento del proyectil.
- **_rebotes**: Cantidad de rebotes que puede tener un proyectil.

Estos atributos pueden mejorarse mediante los métodos `mejorar_*()` y se resetean con `reiniciar_upgrades()`.
