#
# Script to run through all the endpoints
#

print("Running tests")

print("  Testing login...")
import login

print("  Testing logout...")
import logout

print("  Testing get all cereals...")
import list_all_cereals

print("  Testing get cereals with filter...")
import list_all_filter

print("  Testing get cereals sorted...")
import list_all_sorted

print("  Testing get cereals with select...")
import list_all_select

print("  Testing get one cereal...")
import list_one_cereal

print("  Testing create new cereal...")
import create_cereal

print("  Testing update new cereal...")
import update_cereal

print("  Testing delete new cereal...")
import delete_cereal

print("  Testing image endpoint...")
import get_cereal_image

print("Done! All is good")
