import hlt
import logging
import collections

game = hlt.Game("Piebot_3")
logging.info("startup Piebot_3")



while True:
    game_map = game.update_map()
    my_ships = game.update_map.get_me().all_ships()
    my_planets = game.update_map.get_me().all_planets()
    command_queue = []
    empty_planets = []
    target_planets = []
    target_ships = []

    
    for ship in my_ships:
        shipid = ship.id
        if ship.docking_status != ship.DockingStatus.UNDOCKED: #if ship docked, will skip
            continue


        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = collections.OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))

        close_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]
        close_enemy_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0] not in my_planets]
        close_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in my_ships]

        for planet in empty_planets:
            if planet.is_owned():
                continue

            if ship.can_dock(planet):
                command_queue.append(ship.dock(planet))
            else:
                if planet in empty_planets:
                    navigate_command = ship.navigate(
                    ship.closest_point_to(planet),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=True)
                else:
                    for enemy_planet in enemy_planets:
                        navigate_command = ship.navigate(
                        ship.closest_point_to(planet),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=True)

                if navigate_command:
                    command_queue.append(navigate_command)

            break

    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
