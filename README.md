In Divinity: Original Sin 1, distributing gear was easy because there was only
the armor value to consider.  DOS2 complicates this because gear has a physical
armor value and a magic armor value.  Trying to find the best balance / gear
distribution is a bit annoying!  This script solves that.

To use it, start by stripping off all your armor across all characters into
columns in your inventory.  Then pre-allocate gear based on constraints.  So
if you have chest pieces that have a minimum strength or intelligence
requirement that only one or two characters can actually use, pre-place them.
Doing that reduces the search space for optimizing distribution of the remaining
gear, which is the whole point of this script.

Those pre-placements will be baked into the "physical" and "magic" starting
character values.  Similarly, if you have one character running one hand weapon
plus shield, the armor value of the shield will be baked into the starting
values.  The script doesn't even need to worry about that, so it reduces the
search space and execution time.

Using this script means manipulating the characters and available_gear arrays,
and nested dicts in python.  If you're here, you know what that means, and
you'll figure it out.  :-D

If a particular gear slot is already locked down, set it to None in the
character record.  That means its armor values are already baked into the
character baseline "physical" and "magic".  The script will treat those as
off-limits.  This is the mechanism for reducing search space and execution time
as mentioned above.

A note about memory management: because the search space is absolutely massive,
potentially up to hundreds of millions of permutations, the script keeps track
of what permutations it has already evaluated.  To put it simply, assigning
chest 1 to character A then boots 3 to character B is exactly the same as
assigning boots 3 to character B then chest 1 to character A.  To avoid all the
redundant work that would arise from fully exploring the optimal solution search
space, the script keeps track of what permutations it has already evaluated.
Because there are potentially hundreds of millions of them, it uses a hash value
for each possible solution, and a very large bitmap to keep track of which ones
it's already evaluated.  Why not just use a set, you ask?  That would run out
of memory far sooner.  If the script is dying on you due to out of memory,
reduce already_evaluated_sig_hash_num_bits.  As with setting up the initial
conditions, if you're here, you know what that means, and you'll figure it out.

There is only one command line option:

-d X: this is for progress visibility.  X is the recursion depth to which the
script will print progress lines.  Those lines look like this:

d=2 c=3 t=38.474005     n=330566     |     type: 6 of 6 (shoes gloves pants belt ring *necklace) item: 1 of 1 (*SN)
d=1 c=1 t=38.474296     n=330567     |   type: 1 of 6 (*shoes gloves pants belt ring necklace) item: 1 of 4 (*MS BSB TS2 TS1)
d=2 c=0 t=38.474325     n=330568     |     type: 1 of 6 (*shoes gloves pants belt ring necklace) item: 1 of 3 (*BSB TS2 TS1)

d= tells you the recursion depth.  c= tells you which character index the script
is currently considering.  t= tells you the elapsed time.  n= tells you how many
gear assignment permutations have been considered thus far.  The last parts,
type: and item: tell you what it's looking at right now.  If you're using this
for progress tracking, you'll see the type march forward (designated by *) and
likewise for item.