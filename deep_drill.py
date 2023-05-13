depth_one = -8.
depth_two = -13.
depth_three = -16.75
depth_four = -19.75

peck_one = .5
peck_two = .4
peck_three = .3
peck_four = .2

drill_rpm = 600
low_rpm = 100
feed_ipm = 4.8
high_ipm = 150.

start_depth = -4.
current_depth = start_depth
hole_depth = -19.75

tool_number = "T51"
staged_tool = "T63"
tool_diameter = .75
work_offset = "G54.1 P11"
index = "B0"
x_location = -9.917
y_location = .72
r_plain = .5
with open('deep_hole.txt', 'w') as w:
    w.write(f"(DRILL {tool_diameter} DEEP HOLE)\n")
    w.write(f"{tool_number} {staged_tool} M06 (LONG {tool_diameter} DRILL)\n")
    w.write(f"G00 G90 {work_offset} X{x_location} Y{y_location} {index}.\n")
    w.write(f"G43 Z{r_plain}\n")
    w.write("\n")
    while current_depth >= hole_depth:
        if current_depth >= depth_one:
            w.write(f"M04 S{low_rpm}\n")
            w.write(f"G01 Z{round(current_depth + .25, 3)} F{high_ipm}\n")
            w.write(f"M51\n")
            w.write(f"S{drill_rpm} M03\n")
            w.write(f"Z{round(current_depth - peck_one, 3)} F{feed_ipm}\n")
            current_depth = round(current_depth - peck_one, 3)
            w.write(f"Z{round(current_depth + .1, 3)}\n")
            w.write(f"S{low_rpm} M03\n")
            w.write(f"Z{r_plain} F{high_ipm}\n")
            w.write(f"M05\n")
            w.write(f"M09\n")
            w.write(f"M01 (BLOW CHIPS OUT OF HOLE)\n")
            w.write("\n")
        elif current_depth <= depth_one and current_depth >= depth_two:
            w.write(f"M04 S{low_rpm}\n")
            w.write(f"G01 Z{round(current_depth + .25, 3)} F{high_ipm}\n")
            w.write(f"M51\n")
            w.write(f"S{drill_rpm} M03\n")
            w.write(f"Z{round(current_depth - peck_two, 3)} F{feed_ipm}\n")
            current_depth = round(current_depth - peck_two, 3)
            w.write(f"Z{round(current_depth + .1, 3)}\n")
            w.write(f"S{low_rpm} M03\n")
            w.write(f"Z{r_plain} F{high_ipm}\n")
            w.write(f"M05\n")
            w.write(f"M09\n")
            w.write(f"M01 (BLOW CHIPS OUT OF HOLE)\n")
            w.write("\n")
        elif current_depth <= depth_two and current_depth >= depth_three:
            w.write(f"M04 S{low_rpm}\n")
            w.write(f"G01 Z{round(current_depth + .25, 3)} F{high_ipm}\n")
            w.write(f"M51\n")
            w.write(f"S{drill_rpm} M03\n")
            w.write(f"Z{round(current_depth - peck_three, 3)} F{feed_ipm}\n")
            current_depth = round(current_depth - peck_three, 3)
            w.write(f"Z{round(current_depth + .1, 3)}\n")
            w.write(f"S{low_rpm} M03\n")
            w.write(f"Z{r_plain} F{high_ipm}\n")
            w.write(f"M05\n")
            w.write(f"M09\n")
            w.write(f"M01 (BLOW CHIPS OUT OF HOLE)\n")
            w.write("\n")
        elif current_depth <= depth_three:
            w.write(f"M04 S{low_rpm}\n")
            w.write(f"G01 Z{round(current_depth + .25, 3)} F{high_ipm}\n")
            w.write(f"M51\n")
            w.write(f"S{drill_rpm} M03\n")
            w.write(f"Z{round(current_depth - peck_four, 3)} F{feed_ipm}\n")
            current_depth = round(current_depth - peck_four, 3)
            w.write(f"Z{round(current_depth + .1, 3)}\n")
            w.write(f"S{low_rpm} M03\n")
            w.write(f"Z{r_plain} F{high_ipm}\n")
            w.write(f"M05\n")
            w.write(f"M09\n")
            w.write(f"M01 (BLOW CHIPS OUT OF HOLE)\n")
            w.write("\n")
        else:
            print("error")
            break
    w.write(f"Y10.\n")
    w.write("G91 G28 Z0.\n")
    w.write("M00\n")


    
        