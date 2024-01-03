# Ion-Ramjet-Beta
 A physics simulation to model to effectiveness of a prosposed method of interstellar travel: ion ramjets. An ion ramjet uses the proven technology of ion thrusters in combination with the still sci-fi magnetic scoop to pick up fuel as it travels in the form of hydrogen from the insterstellar medium (ISM).


# Data Storage Format
 Data is stored as a string of Python dictionaries. Each line corresponds to one step of the simulation, aside from line 0 which is some initial data, such as the simulation rate. Here is the format of stored data:
    # 0: {
    #   'step': $step_size
    #   'name': $ramjet_name
    # }
    # $step_number: {
    #   'steps':        $current_step,
    #   'sim_time':     $sim_time_elapsed,
    #   'real_time':    $real_time_elapsed,
    #   'ramjet': {
    #       'mass':         $ramjet_mass,
    #       'name':         $ramjet_name,
    #       'spacetime': {
    #           'time':     $time_experienced
    #           'pos_x':    $x_position,
    #           'pos_y':    $y_position,
    #           'vel_x':    $x_velocity,
    #           'vel_y':    $y_velocity,
    #           'acc_x':    $x_acceleration,
    #           'acc_y':    $y_acceleration
    #       },
    #       'parts': {
    #           '$tank': {
    #               'fuel':             $fuel,
    #               'capacity':         $capacity
    #           },
    #           '$battery': {
    #               'fuel':             $fuel,
    #               'capacity':         $capacity
    #           },
    #           '$thruster': {
    #               'thrust':           $thrust.hypo(),
    #               'fuel':             $fuel_consumed,
    #               'fuel_throttle':    $fuel_throttle,
    #               'power':            $power_consumed,
    #               'power_throttle':   $power_throttle
    #           },
    #           '$scoop': {
    #               'm_H':              $mass_of_H_scooped,
    #               'power':            $power_consumed,
    #               'power_throttle':   $power_throttle,
    #               'allignment':       $allignment_of_n_v,
    #               'area':             $effective_scoop_area,
    #               'volume':           $volume_swept
    #           },
    #           '$generator': {
    #               'power':            $power_generated
    #           }
    #       }
    #   }
    # }
