from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

import re

from vehicles.forms import VehicleSearchForm
from vehicles.models import Automobile

def get_vsn_permutations(s):
    results = []

    # Holds all of the strings that will act as base strings for all future
    # permutations.
    base_queue = [s]

    # While there are still base strings to be used for new permutations,
    # continue to add to the permutation results and generating new base
    # strings 
    while len(base_queue):
        current = base_queue.pop()
        
        # Add the current base string as a possible permutation
        results.append(current)  

        # We look for the first occurrence of a wildcard and set it as our
        # starting point for modifying the base string because modifying prior
        # to that will cause duplicates. I THINK THIS NEEDS TO USE THE INDEX OF
        # THE LAST '*' AS OPPOSED TO THE FIRST
        start = current.find('*') + 1

        for i in range(start, len(current)):
            # Since we started off with a base without any wildcards, we are
            # only interested in making modifications where we can add
            # wildcards
            if not current[i] == '*':
                prefix = current[0:i]
                suffix = current[i + 1:]

                new_base = '*'.join([prefix, suffix])

                base_queue.append(new_base)

    # I CURRENTLY HAVE A BUG THAT CREATES DUPLICATE PERMUTATIONS. TEMPORARILY
    # I HAVE MADE THE RESULTS A SET TO "FIX" THE ISSUE BUT I SHOULD COME BACK
    # AND MAKE THE NECESSARY CHANGES. I STILL MAY WANT TO CONSIDER USING A SET 
    # AS A PRECAUTION.
    return set(results)

def get_vsn_best_matches(potential_matches):
    best_matches = None
    wildcard_match_map = {}

    wildcard_regex = r'[*]'
    for match in potential_matches:
        wildcard_count = len(re.findall(wildcard_regex, match.serial_number))

        #if not wildcard_count:
        #    wildcard_count = 0
    
        if wildcard_count in wildcard_match_map:
            wildcard_match_map.get(wildcard_count).append(match)
        else:
            match_list = [match]

            wildcard_match_map[wildcard_count] = match_list

    for max_wild in range(0, 13):
        if max_wild in wildcard_match_map:
            best_matches = wildcard_match_map.get(max_wild)
            break;

    return best_matches 

def get_vsn_prefix_query(prefix_base):
    prefixes = get_vsn_permutations(prefix_base)
    
    prefix_query = None
    for prefix in prefixes:
        if prefix_query:
            prefix_query = prefix_query | Q(serial_number__startswith=prefix)
        else:
            prefix_query = Q(serial_number__startswith=prefix)

    return prefix_query

def get_vsn_suffix_query(suffix_base):
    suffixes = get_vsn_permutations(suffix_base)
    
    suffix_query = None
    for suffix in suffixes:
        if suffix_query:
            suffix_query = suffix_query | Q(serial_number__endswith=suffix)
        else:
            suffix_query = Q(serial_number__endswith=suffix)

    return suffix_query

def vehicle_search(request):
    template_vars = {}

    if request.method == 'POST':
       form = VehicleSearchForm(request.POST)

       if form.is_valid():
           vsn = form.cleaned_data['vsn']
           midpoint = len(vsn) / 2

           prefix_query = get_vsn_prefix_query(vsn[0:midpoint])
           suffix_query = get_vsn_suffix_query(vsn[midpoint:])

           potential_matches = Automobile.objects.filter(prefix_query).filter(suffix_query)

           best_matches = get_vsn_best_matches(potential_matches)

           template_vars['matches'] = best_matches
           template_vars['vsn'] = vsn
    else:
       form = VehicleSearchForm()

    template_vars['form'] = form

    return render_to_response('vehicleSearch.html', template_vars, context_instance=RequestContext(request))
