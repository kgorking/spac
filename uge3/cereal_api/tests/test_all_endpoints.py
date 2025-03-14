#
# Script to run through all the endpoints
#

print("Running tests...")

print("  login")
import login

print("  logout")
import logout

print("  getting all cereals")
import list_all_cereals

print("  getting cereals with filter")
import list_all_filter

print("  getting cereals sorted")
import list_all_sorted

print("  getting one cereal")
import list_one_cereal

print("  create new cereal")
import create_cereal

print("  update new cereal")
import update_cereal

print("  delete new cereal")
import delete_cereal

print("  image endpoint")
import get_cereal_image

print("Done! All is good")
