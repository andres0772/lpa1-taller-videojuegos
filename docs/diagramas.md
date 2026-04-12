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
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ + hp_max: int {property}                                                                     │
│ + hp_actual: int {property}                                                                  │
│ + ataque: int {property}                                                                     │
│ + defensa: int {property}                                                                   │
│ + esta_vivo(): bool {abstract}                                                              │
│ + recibir_daño(daño: int): None                                                             │
│ + curar(cantidad: int): None                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
                  ▲                                           ▲
                  │                                           │
                  │ extends                                   │ extends
                  │                                           │
┌─────────────────┴─────────────────────────────────────────┐ ┌─────────────────────────────┐
│                  Personaje                                   │          Enemigo             │
├─────────────────────────────────────────────────────────────┤ ├────���────────────────────────┤
│ - _nombre: str                                               │ - _nombre: str             │
│ - _nivel: int                                                 │ - _tipo: Literal           │
│ - _experiencia: int                                           │ - _experiencia_al_derrotar │
│ - _experiencia_siguiente_nivel: int                            │ - _oro_al_derrotar: int     │
│ - _oro: int                                                   │ - _es_jefe: bool           │
│ - _inventario: list[Item]                                    │ - center_x: float         │
│ - _arma_equipada: Optional[Equipamiento]                     │ - center_y: float          │
│ - _armadura_equipada: Optional[Equipamiento]                 │                            │
├─────────────────────────────────────────────────────────────┤ ├─────────────────────────────┤
│ + nombre: str {property}                                     │ + nombre: str {property}   │
│ + nivel: int {property}                                      │ + tipo: str {property}     │
│ + experiencia: int {property}                               │ + experiencia_al_derrotar   │
│ + experiencia_siguiente_nivel: int {property}               │ + oro_al_derrotar: int     │
│ + oro: int {property}                                        │ + es_jefe: bool {property}  │
│ + inventario: list[Item] {property}                            │ + esta_vivo(): bool        │
│ + arma_equipada: Optional[Equipamiento] {property}             │                           │
│ + armadura_equipada: Optional[Equipamiento] {property}      │                           │
│ + ataque_total: int {property}             ◄───>           │                           │
│ + defensa_total: int {property}            │                │                           │
│ + esta_vivo(): bool                                     │                │                           │
│ + ganar_experiencia(xp: int): None             SistemaCombate │                │                           │
│ + _subir_nivel(): None                         calcular_daño  │                │                           │
│ + agregar_item(item: Item): None               attacking      │                │                           │
│ + usar_item(item: Item): bool                                              │                           │
│ + equipar(equipamiento: Equipamiento): None                 │                │                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

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
            ▲                    ▲                    ▲                    ▲
            │                    │                    │                    │
            │ extends           │ extends           │ extends           │ extends
            │                    │                    │                    │
┌───────────┴───────────┐ ┌────┴───────────┐ ┌┴───────────┐ ┌┴───────────────────┐
│   Equipamiento        │ │   Consumible │ │   Tesoro    │ │  TrampaExplosiva   │
├──────────────────────┤ ├───────────────┤ ├─────────────┤ ├─────────────────────┤
│ - _tipo: str         │ │ - _efecto    │ │ - _valor   │ │ - _daño: int        │
│ - _bonus: int        │ │ - _precio    │ │ - _precio  │ │ - _alcance: int     │
│ - _precio: int       │ │              │ │ - center_x │ │                     │
│                      │ │              │ │ - center_y │ │                     │
├──────────────────────┼─┼──────────────┼─┼────────────┼┼─────────────────────┤
│ + tipo: str {prop}   │ │ + efecto     │ │ + valor    ││ + daño: int {prop}   │
│ + bonus: int {prop}  │ │   : int     │ │   : int   ││ + alcance: int {prop}
│ + precio: int {prop}│ │ + precio    │ │ + precio  ││ + usar(): bool      │
│ + usar(): bool      │ │   : int     │ │ + usar()  │ │ + activar(): None  │
│ + vender(): int     │ │ + usar()    │ │ + vender()│ │                     │
│                      │ │ + vender()   │ │   : int   │ │                     │
└──────────────────────┴─┴──────────────┴─┴────────────┴┴─────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       SISTEMAS                                              │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                         SistemaCombate                                │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ + _obtener_ataque_total(entidad: Entidad): int                         │
│ + _obtener_defensa_total(entidad: Entidad): int                      │
│ + calcular_daño(ataque: int, defensa: int): int                       │
│ + atacar(atacante: Entidad, defensor: Entidad): ResultadoCombate        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────┐ ┌─────────────────────────────────────┐
│    SistemaExperiencia         │ │      SistemaInventario                │
├─────────────────────────────┤ ├─────────────────────────────────────┤
│ + EXP_BASE: int = 100         │ │ + agregar_item(inventario, item): None    │
│ + MULT_NIVEL: int = 1.5   │ │ + usar_item(inventario, indice,     │
│ + experiencia_para_nivel  │ │   personaje): bool                │
│   (nivel: int): int        │ │ + vender_item(inventario, indice, │
│ + puede_subir_nivel():bool│ │   personaje): Optional[int]      │
│ + nivel_por_experiencia() │ │ + comprar_item(inventario, item, │
│   : int                   │ │   personaje): bool                │
└─────────────────────────────┘ └─────────────────────────────────────┘

┌─────────────────────────────┐ ┌─────────────────────────────────────┐
│       SistemaTienda           │ │      ItemTienda (辅助类)             │
├─────────────────────────────┤ ├─────────────────────────────────────┤
│ + ITEMS_TIENDA: list         │ │ - equipamiento: Equipamiento        │
│ + getter_items_tienda(): list  │ │ - stock: int                        │
│ + comprar_item(): tuple     │ │                                   │
│ + vender_item(): tuple       │ │ + nombre: str {property}            │
└─────────────────────────────┘ │ + precio: int {property}           │
                               │ + tipo: str {property}            │
                               │ + bonus: int {property}           │
                               └─────────────────────────────────────┘


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
│ + alto: int {property}                                                             │
│ + enemigos: list[Enemigo] {property}                                               │
│ + items: list[Item] {property}                                                     │
│ + _generar_contenido(): None                                                       │
│ + _generar_enemigos(cantidad: int): None                                           │
│ + _generar_items(cantidad: int): None                                              │
│ + agregar_enemigo(enemigo: Enemigo): None                                         │
│ + agregar_item(item: Item): None                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                          UI                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│              HUD                   │         MenuPausa              │      MenuTienda    │
├─────────────────────────────┤ ├───────────────────────────────┤ ├─────────────────┤
│ - _personaje: Personaje       │ │ - _personaje: Personaje       │ │ - _personaje    │
│                            │ │ - _modo_actual: str         │ │ - _escenario   │
│                            │ │                             │ │ - _modo_actual │
│                            │ │ + abierto: bool {property}  │ │ - _mensaje     │
│ + dibujar(): None          │ │ + abrir(): None             │ │                 │
│                            │ │ + cerrar(): None            │ │ + abierto      │
│                            │ │ + manejar_input(key): bool  │ │   : bool       │
│                            │ │ + dibujar(): None           │ │ + abrir(): None│
│                            │ │                             │ │ + cerrar()     │
│                            │ │                             │ │ + manejar_     │
│                            │ │                             │ │   input():bool│
│                            │ │                             │ │ + dibujar()    │
└─────────────────────────────┘ └───────────────────────────────┘ └─────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                               RELACIONES CLAVE                                             │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  Personaje ──────────► Item (usa)                                                    │
│       │                                                                              │
│       │ tiene (inventario: list[Item])                                               │
│       ▼                                                                              │
│  Equipamiento ◄──────► Personaje (equipar)                                          │
│                                                                                      │
│  Personaje ──────────► Enemigo (atacar)                                              │
│       │                    │                                                         │
│       │                    │ derrotado da XP/ORO                                      │
│       │◄───────────────────┘                                                      │
│       │                                                                         │
│       │                                                                         │
│  Escenario ──────────► Area                                                         │
│       │                    │                                                      │
│       │                    │ contiene                                             │
│       ▼                    ▼                                                      │
│  Enemigo ◄─────────── Item                                                         │
│                                                                                      │
│  SistemaCombate ◄─────────► Entidad (calcula daño)                                 │
│                                                                                      │
│  SistemaTienda ◄─────── Personaje (compra/vende)                                   │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Descripción de las Relaciones

###Herencia (Generalización)

- **Entidad** → Clase abstracta base de la cual heredan `Personaje` y `Enemigo`. Define los atributos comunes: HP, ataque, defensa.
- **Item** → Clase abstracta base de la cual heredan `Equipamiento`, `Consumible`, `Tesoro` y `TrampaExplosiva`.

###Asociación

- **Personaje** ↔ **SistemaCombate**: El personaje puede atacar y recibir ataques a través del sistema de combate.
- **Personaje** ↔ **SistemaExperiencia**: Gestiona la experiencia y nivelación.
- **Personaje** ↔ **SistemaInventario**: Gestiona el inventario.
- **Personaje** ↔ **SistemaTienda**: Permite comprar y venderitems.
- **Escenario** ↔ **Area**: Un escenario contiene múltiples áreas.

###Agregación

- **Personaje** → **Inventario** (list[Item]): El personaje tiene un inventario.
- **Area** → **Enemigos** (list[Enemigo]): El área contiene enemigos.
- **Area** → **Items** (list[Item]): El área contieneitems.

###Composición

- **Escenario** → **Area**: El escenario gestiona las áreas. Si el escenario se destruye, las áreas también.

## Notas de Diseño

1. **Patrón Strategy implícito**: `SistemaCombate` actúa como una clase utilitaria estática que encapsula la lógica de combate.
2. **Patrón Observer implícito**: El `HUD` observa al `Personaje` para actualizar la UI cuando cambian los stats.
3. **Patrón Factory implícito**: `Area._generar_enemigos()` y `Area._generar_items()` actúan como factories para crear contenido.
4. **Encapsulamiento**: Uso de properties para proteger los atributos privados.
5. **Herencia vs Composición**: Se usa herencia para entidades del dominio (Personaje, Enemigo, Items) y composición para sistemas (SistemaCombate, SistemaTienda).

