#!/usr/bin/python

import argparse

def validate( parameters ):
    if parameters.water and parameters.coffee and parameters.ratio:
        return "Must specify only water+coffee, water+ratio, coffee+ratio - can't specify all three"
    return None

def fix_ratio( ratio ):
    """ allows user to pass ratio as coffee/water OR water/coffee - but we'll normalize to coffee/water """
    if ( ratio and ratio > 1 ):
        return 1/ratio;
    return ratio;

def normalize( parameters ):
    water = 210
    coffee = 15

    if ( parameters.water and parameters.coffee ):
        water = parameters.water
        coffee = parameters.coffee
    elif ( parameters.water and parameters.ratio ):
        water = parameters.water
        coffee = int( round( water * fix_ratio( parameters.ratio ) ) )
    elif ( parameters.coffee and parameters.ratio ):
        water = int( round( coffee / fix_ratio( parameters.ratio ) ) )
        coffee = parameters.coffee
    
    return ( water, coffee )

def water_for_bloom( coffee ):
    """ fact: coffee holds twice its weight in water """
    return coffee * 2

def to_seconds( timestr ):
    (m,s) = [int(n) for n in timestr.split( ":" )]
    return m*60 + s

def fmt_seconds( seconds ):
    return "%d:%02d" % (seconds/60, seconds%60)

def summary_str( water, coffee, pour_time_sec ):
    return "water: %dg, coffee: %dg, ratio: %.03f, time: %s" % ( water, coffee, float(coffee)/float(water), fmt_seconds(pour_time_sec) );

def print_steps( water, coffee, pour_time_sec, bloom_time_sec, increments ):
    step_fmt = "%8s %8s" # sec grams
    print step_fmt % ( "TIME", "GRAMS" )

    timer = 0
    bloom_water = water_for_bloom( coffee )
    water_remaining = water - bloom_water
    print step_fmt % ( timer, bloom_water )

    water_per_step = 0
    while round(water_remaining) > 0:
        if ( timer == 0 ):
            # the 1st post-bloom pour will be same as bloom
            water_remaining -= bloom_water
            timer = bloom_time_sec

            step_count = float(pour_time_sec-timer) / float(increments)
            water_per_step = float(water_remaining) / float(step_count)
        elif ( timer + increments > pour_time_sec ):
            water_remaining = 0
            timer = pour_time_sec
        else:
            water_remaining = water_remaining - water_per_step
            timer = timer + increments
        print step_fmt % ( fmt_seconds(timer), "%d" % round(water-water_remaining) )

def print_coffee_info( parameters ):
    ( water, coffee ) = normalize( parameters )
    pour_time_sec = to_seconds( parameters.pour_time )
    print( summary_str( water, coffee, pour_time_sec ) )
    print_steps( water, coffee, pour_time_sec, parameters.bloom_time, parameters.second_increments )

def main():
    parser = argparse.ArgumentParser(description='Calculate optimal coffee pour-over times')
    parser.add_argument( '-w','--water', type=int, help="Desired amount of water to use (g/ml)" )
    parser.add_argument( '-c','--coffee', type=int, help="Desired grams of coffee to use" )
    parser.add_argument( '-r','--ratio', type=float, help="Desired coffee:water (eg 0.07) or water:coffee (eg 14) ratio" )
    parser.add_argument( '-p','--pour_time', default="2:30", help="Time until the last pour of the kettle" )
    parser.add_argument( '-b','--bloom_time', type=int, default="30", help="How many seconds for initial bloom" )
    parser.add_argument( '-s','--second_increments', type=int, default="10", help="Increments to show (eg every 10 seconds)" )
    parameters = parser.parse_args() 

    errors = validate( parameters )
    if ( errors ):
        print errors
        exit( 1 )
    print_coffee_info( parameters )

if __name__ == "__main__":
    main()
