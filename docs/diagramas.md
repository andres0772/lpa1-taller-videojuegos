# Diagramas del Proyecto

## Diagrama de Clases

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      ENTIDADES                                             │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                   <<abstract>>                                             │
│                                    Entidad                                                  │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ - _hp_max: int                                                                              │
│ - _hp_actual: int                                                                            │
│ - _ataque: int                                                                               │
│ - _defensa: int                                                                              │
│ - _sprite: Optional[Sprite]                                                                  │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ + hp_max: int {property}                                                                     │
│ + hp_actual: int {property}                                                                  │
│ + ataque: int {property}                                                                     │
│ + defensa: int {property}                                                                   │
│ + ataque_total: int {property}    ◄─────────── nuevo                                         │
│ + defensa_total: int {property}   ◄─────────── nuevo                                         │
│ + esta_vivo(): bool {abstract}                                                              │
│ + recibir_daño(daño: int): None                                                             │
│ + curar(cantidad: int): None                                                                 │
│ + tiene_sprite(): bool ◄─────────────────── nuevo                                              │
│ + puede_recibir_daño(): bool {abstract} ◄─── nuevo                                           │
│ + puede_ser_destruido(): bool {abstract} ◄─── nuevo                                         │
│ + sprite: Optional[Sprite] {property} ◄─── nuevo                                           │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
                   ▲                                           ▲
                   │                                           │
                   │ extends                                   │ extends
                   │                                           │
┌─────────────────┴─────────────────────────────────────────┐ ┌─────────────────────────────┐
│                  Personaje                                   │          Enemigo             │
├─────────────────────────────────────────────────────────────┤ ├─────────────────────────────┤
│ - _nombre: str                                               │ - _nombre: str             │
│ - _nivel: int                                                 │ - _tipo: Literal           │
│ - _experiencia: int                                           │ - _experiencia_al_derrotar │
│ - _experiencia_siguiente_nivel: int                            │ - _oro_al_derrotar: int     │
│ - _oro: int                                                   │ - _es_jefe: bool           │
│ - _inventario: list[Item]                                    │ - _sprite: Optional[Sprite]│
│ - _arma_equipada: Optional[Equipamiento]                     │ - center_x: float          │
│ - _armadura_equipada: Optional[Equipamiento]                 │ - center_y: float          │
│ - _velocidad_disparo: float ◄─────────── nuevo               │                           │
│ - _dano_proyectil: float ◄──────────── nuevo                  ├─────────────────────────────┤
│ - _velocidad_proyectil: float ◄───────── nuevo                  │ + nombre: str {property}   │
│ - _rebotes: int ◄───────────────── nuevo                      │ + tipo: str {property}    │
├─────────────────────────────────────────────────────────────┤ │ + experiencia_al_derrotar   │
│ + nombre: str {property}                                     │ + oro_al_derrotar: int     │
│ + nivel: int {property}                                      │ + es_jefe: bool {property}  │
│ + experiencia: int {property}                               │ + esta_vivo(): bool        │
│ + experiencia_siguiente_nivel: int {property}               │ + tiene_sprite(): bool ◄─── nuevo│
│ + oro: int {property}                                        │ + sprite: Optional[Sprite]◄─nuevo│
│ + inventario: list[Item] {property}                            │                           │
│ + arma_equipada: Optional[Equipamiento] {property}             │                           │
│ + armadura_equipada: Optional[Equipamiento] {property}      │                           │
│ + ataque_total: int {property}             ◄───>           │                           │
│ + defensa_total: int {property}            │                │                           │
│ + esta_vivo(): bool                                     │                │                           │
│ + cooldown_disparo: float {property} ◄─ nuevo            │                │                           │
│ + ganar_experiencia(xp: int): None             SistemaCombate │                │           │
│ + _subir_nivel(): None                         calcular_daño  │                │           │
│ + agregar_item(item: Item): None               attacking      │                │           │
│ + usar_item(item: Item): bool                   ◄───────────────►│                │           │
│ + equipar(equipamiento: Equipamiento): None                 │                │           │
│ + agregar_oro(cantidad: int): None ◄─────────── nuevo         │                │           │
│ + quitar_oro(cantidad: int): None ◄─────────── nuevo           │                │           │
│ + mejorar_velocidad_disparo(): None ◄───────── nuevo           │                │           │
│ + mejorar_dano_proyectil(): None ◄─────────── nuevo           │                │           │
│ + mejorar_velocidad_proyectil(): None ◄───── nuevo             │                │           │
│ + mejorar_rebote(): None ◄───────────────── nuevo              │                │           │
│ + reiniciar_upgrades(): None ◄──────────────── nuevo           │                │           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      PROYECTILES                                           │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                   Proyectil                                               │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ - _direccion_x: float                                                                        │
│ - _direccion_y: float                                                                        │
│ - _dano: float                                                                               │
│ - velocidad: float                                                                          │
│ - es_del_jugador: bool                                                                       │
│ - sprite: Sprite                                                                             │
│ - activo: bool                                                                               │
│ - _rebotes_maximos: int                                                                       │
│ - _rebotes_actuales: int                                                                     │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ + esta_vivo(): bool                                                                          │
│ + puede_recibir_daño(): bool ◄──────────────────────────────────────────────────────────────┤
│ + puede_ser_destruido(): bool ◄─────────────────────────────────────────────────────────────┤
│ + actualizar(): None                                                                        │
│ + esta_fuera_de_pantalla(): bool                                                            │
│ + tiene_sprite(): bool                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        ITEMS                                               │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                 <<abstract>>                                             │
│                                   Item                                                   │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ - _nombre: str                                                                       │
│ - _descripcion: str                                                                  │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ + nombre: str {property}                                                             │
│ + descripcion: str {property}                                                        │
│ + usar(personaje: Personaje): bool {abstract}                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
              ▲                    ▲                    ▲                    ▲                    ▲
              │                    │                    │                    │                    │
              │ extends           │ extends           │ extends           │ extends           │ extends
              │                    │                    │                    │                    │
┌─────────────┴──────────┐ ┌────┴──────────┐ ┌───┴──────────┐ ┌───┴──────────────────┐┴──────────┐
│    Equipamiento         │ │  Consumible   │ │   Tesoro     │ │  TrampaExplosiva    ││ ItemDrop  │
├─────────────────────────┤ ├───────────────┤ ├──��─��────────┤ ├──────────────────────┤├───────────┤
│ - _tipo: str          │ │ - _efecto     │ │ - _valor    │ │ - _daño: int        ││- _tipo: str│
│ - _bonus: int        │ │ - _precio    │ │ - _precio   │ │ - _alcance: int    ││- _valor   │
│ - _precio: int       │ │              │ │ - center_x  │ │                    ││- _tiempo_ex│
│                      │ │              │ │ - center_y │ │                    ││- _sprites │
│                      │ │              │ │            │ │                    ││           │
├──────────────────────┼─┼──────────────┼─┼────────────┼┼────────────────────┼┼───────────┤
│ + tipo: str {prop}   │ │ + efecto     │ │ + valor    ││ + daño: int {prop}  ││+ tipo     │
│ + bonus: int {prop}  │ │   : int     │ │   : int   ││ + alcance: int {prop}││ {property}│
│ + precio: int {prop}│ │ + precio    │ │ + precio  ││ + usar(): bool     ││+ valor    │
│ + usar(): bool      │ │   : int     │ │ + usar()  │ │ + activar(): None  ││ {property}│
│ + vender(): int     │ │ + usar()    │ │ + vender()│ │                    ││+ expiro   │
│                      │ │ + vender()   │ │   : int   │ │                    ││ : bool    │
│                      │ │              │ │           │ │                    ││+ crear_   │
│                      │ │              │ │           │ │                    ││ desde_    │
│                      │ │              │ │           │ │                    ││ enemigo() │
│                      │ │              │ │           │ │                    ││+ recoger()│
│                      │ │              │ │           │ │                    ││: None     │
│                      │ │              │ │           │ │                    ││+ actuali- │
│                      │ │              │ │           │ │                    ││ zar_tiem- │
│                      │ │              │ │           │ │                    ││ po():None │
│                      │ │              │ │           │ │                    ││+ tiene_  │
│                      │ │              │ │           │ │                    ││ sprite() │
└──────────────────────┴─┴──────────────┴─┴────────────┴┴────────────────────┴┴───────────┘
                                             ▲
                                             │
                                             │ extends
                                             │
              ┌──────────────────────────────┐ ┌──┴──────────────────────────────┐
              │    MejoraProyectil          ├─────────────────────────────────────────┤
              ├────────────────────────────┤ │ - _tipo: str                       │
              │ - _tipo: str              │ │ - _descripcion: str                 │
              │ - _descripcion: str      │ │                                   │
              ├───────────────────────────-│ │ + usar(personaje: Personaje): bool  │
              │ + usar(personaje: Personaje) │ │   ◄───────────────────────────────┘
              │   : bool                  │ │
              └──────────────────────────┘ │


┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        SERVICIOS                                            │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                              GestorProyectiles                              │  GestorCombate      │
├─────────────────────────────────────────────────────────────────────────────┤ ├───────────────────┤
│ - _ancho: int                                               │ │ + _cooldown: float │
│ - _alto: int                                                │ │                   │
│ - proyectiles: list[Proyectil]                             │ ├───────────────────┤
│ - lista_sprites: list                                       │ │ + verificar_      │
│ - _timers_disparo_enemigo: list                             │ │   combate(atacan- │
│ - _cooldown_jugador: float                                  │ │   te, defensor):  │
│                                                         │ │   bool            │
├─────────────────────────────────────────────────────────────┤ │ + actualizar_    │
│ + crear_proyectil_jugador(...): Proyectil                   │ │   cooldown(dt)   │
│ + crear_proyectil_enemigo(...): Proyectil                    │ │ + puede_combatir- │
│ + actualizar_proyectiles(dt): None ◄─────────────────────► │ │   (): bool        │
│ + verificar_colisiones_enemigos(...): None                 │ │ + procesar_derro- │
│ + eliminar_proyectil(...): None                            │ │   ta_enemigo(...) │
│ + eliminar_enemigo(...): None                               │ └───────────────────┘
│ + limpiar(): None                                          │
└─────────────────────────────────────────────────────────────┘

              ┌──────────────────────────────────────────────┐
              │              GestorItems                    │
              ├──────────────────────────────────────────────┤
              │                                             │
              ├──────────────────────────────────────────────┤
              │ + verificar_colisiones(...): None         │
              │ + procesar_tesoro(...): None               │
              │ + procesar_trampa(...): None                │
              └──────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         MUNDO                                              │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                               Escenario                                       │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ - _ancho: int                                                                      │
│ - _alto: int                                                                       │
│ - _areas: dict[str, Area]                                                             │
│ - _area_actual: str                                                                 │
│ - _nivel: int                                                                      │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ + nivel: int {property}                                                             │
│ + ancho: int {property}                                                             │
│ + alto: int {property}                                                              │
│ + area_actual: str {property}                                                        │
│ + area: Area {property}                                                             │
│ + enemigos: list {property}                                                         │
│ + items: list {property}                                                            │
│ + area_actual.nombre: str {property}                                                 │
│ + areas_disponibles: list[str] {property}                                            │
│ + cambiar_area(tipo: str): bool                                                     │
│ + ir_area_siguiente(): bool                                                         │
│ + ir_area_anterior(): bool                                                          │
│ + agregar_enemigo(enemigo): None                                                   │
│ + agregar_item(item): None                                                          │
│ + regenerar_contenido(): None                                                        │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ contains
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   Area                                               │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ - _tipo: str                                                                       │
│ - _ancho: int                                                                      │
│ - _alto: int                                                                       │
│ - _nivel: int                                                                      │
│ - _enemigos: list[Enemigo]                                                         │
│ - _items: list[Item]                                                                │
│ - _config: dict                                                                   │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ + TIPOS: dict <<class>>                                                              │
│ + tipo: str {property}                                                             │
│ + nombre: str {property}                                                           │
│ + descripcion: str {property}                                                       │
│ + color_fondo: tuple {property}                                                    │
│ + ancho: int {property}                                                            │
│ + alto: int {property}                                                              │
│ + enemigos: list[Enemigo] {property}                                               │
│ + items: list[Item] {property}                                                     │
│ + _generar_contenido(): None                                                       │
│ + _generar_enemigos(cantidad: int): None                                            │
│ + _generar_items(cantidad: int): None                                              │
│ + agregar_enemigo(enemigo: Enemigo): None                                         │
│ + agregar_item(item: Item): None                                                    │
└─────────────────────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                          UI                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│              HUD                   │         MenuPausa              │      MenuTienda    │
├─────────────────────────────┤ ├───────────────────────────────┤ ├─────────────────┤
│ - _personaje: Personaje       │ │ - _personaje: Personaje       │ │ - _personaje    ���
│                            │ │ - _modo_actual: str         │ │ - _escenario     │
│                            │ │                             │ │ - _modo_actual   │
│                            │ │ + abierto: bool {property}  │ │ - _mensaje       │
│ + dibujar(): None          │ │ + abrir(): None             │ │                 │
│                            │ │ + cerrar(): None            │ │ + abierto       │
│                            │ │ + manejar_input(key): bool  │ │   : bool        │
│                            │ │ + dibujar(): None           │ │ + abrir(): None │
│                            │ │                             │ │ + cerrar()      │
│                            │ │                             │ │ + manejar_      │
│                            │ │                             │ │   input():bool  │
│                            │ │                             │ │ + dibujar()     │
└─────────────────────────────┘ └───────────────────────────────┘ └─────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                               RELACIONES CLAVE                                             │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│ ENTIDADES:                                                                          │
│  Entidad ◄─────────────► Personaje (extends)                                          │
│       │                                                                              │
│       │ extends                                                                     │
│       ▼                                                                              │
│  Enemigo                                                                             │
│                                                                                      │
│ PROYECTILES:                                                                         │
│  Entidad ◄─────────────► Proyectil (extends) ────────────────► Sprite              │
│       │                                                                      │       │
│       │                                                                      │ manages│
│       ▼                                                                      ▼        │
│  GestorProyectiles ◄───────────────────────────────────────────────────────────── │
│                                                                                      │
│ ITEMS:                                                                              │
│  Item ◄──────► Equipamiento (extends)                                              │
│    │         ► Consumible (extends)                                               │
│    │         ► Tesoro (extends)                                                  │
│    │         ► TrampaExplosiva (extends)                                         │
│    │         ► ItemDrop (extends) ◄────────────────────────► Enemigo (drop)      │
│    │         ► MejoraProyectil (extends)                                          │
│    │                                                                        │       │
│    └──────────────────────────► GestorItems ◄──────────────────────────────►     │
│                                  Personaje (colecciona)                             │
│                                                                                      │
│ COMBATE:                                                                            │
│  Personaje ──────────► GestorCombate ──────────► Enemigo                             │
│       │                                                                              │
│       │ ataca                                                                       │
│       ▼                                                                              │
│  Proyectil ◄──────────► Enemigo (impacta)                                         │
│                                                                                      │
│ MUNDO:                                                                              │
│  Escenario ◄──────────► Area (contains) ─────────► Enemigo, Item                 │
│                                                                                      │
│ UI:                                                                                 │
│  Personaje ◄──────────────► HUD (observa)                                           │
│       │                  │ MenuPausa                                                │
│       │                  ▼                                                         │
│       └───────────────────► MenuTienda                                              │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Descripción de las Relaciones

###Herencia (Generalización)

- **Entidad** → Clase abstracta base de la cual heredan `Personaje`, `Enemigo` y `Proyectil`. Define los atributos comunes: HP, ataque, defensa, sprite.
- **Item** → Clase abstracta base de la cual heredan `Equipamiento`, `Consumible`, `Tesoro`, `TrampaExplosiva`, `ItemDrop` y `MejoraProyectil`.

###Asociación

- **Personaje** ↔ **GestorCombate**: El personaje puede atacar y recibir ataques a través del gestor de combate.
- **Personaje** ↔ **GestorItems**: Gestiona la colección de items del suelo.
- **GestorProyectiles** ↔ **Proyectil**: Crea y gestiona proyectiles.
- **GestorProyectiles** ↔ **Enemigo**: Verifica colisiones projectile-enemigo.
- **ItemDrop** ↔ **Enemigo**: Los enemigos sueltan items al morir.
- **Escenario** ↔ **Area**: Un escenario contiene múltiples áreas.

###Agregación

- **Personaje** → **Inventario** (list[Item]): El personaje tiene un inventario.
- **GestorProyectiles** → **Proyectiles** (list[Proyectil]): Gestor administra múltiples proyectiles.
- **Area** → **Enemigos** (list[Enemigo]): El área contiene enemigos.
- **Area** → **Items** (list[Item]): El área contiene items.

###Composición

- **Escenario** → **Area**: El escenario gestiona las áreas. Si el escenario se destruye, las áreas también.
- **GestorProyectiles** → **_timers_disparo_enemigo, _cooldown_jugador**: Timers internos del gestor.

## Notas de Diseño

1. **Patrón Service Layer**: `GestorProyectiles`, `GestorCombate` y `GestorItems` actúan como servicios que gestionan lógicas de juego específicas.
2. **Patrón Observer implícito**: El `HUD` observa al `Personaje` para actualizar la UI cuando cambian los stats.
3. **Patrón Factory implícito**: `GestorProyectiles.crear_proyectil_jugador()` y `GestorProyectiles.crear_proyectil_enemigo()` actúan como factories.
4. **Patrón Entity-Component**: Proyectil tiene su propio sprite, lo que permite rendering independiente.
5. **Encapsulamiento**: Uso de properties para proteger los atributos privados.
6. **Herencia vs Composición**: Se usa herencia para entidades del dominio (Personaje, Enemigo, Items, Proyectil) y composición para sistemas (Gestores).
7. **Sistema de Upgrades**: Personaje tiene métodos para mejorar estadísticas de proyectiles (velocidad, daño, rebotes).

## Atributos Nuevos en Personaje (Sistema de Proyectiles)

- **_velocidad_disparo**: Controla la velocidad de fuego del personaje.
- **_dano_proyectil**: Daño base de los proyectiles del personaje.
- **_velocidad_proyectil**: Velocidad de movimiento del proyectil.
- **_rebotes**: Cantidad de rebotes que puede tener un proyectil.

Estos atributos pueden mejorarse mediante los métodos `mejorar_*()` y se resetean con `reiniciar_upgrades()`.