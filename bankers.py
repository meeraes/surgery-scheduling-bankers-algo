import streamlit as st
import numpy as np

def is_safe(available, max_need, allocation, num_processes, num_resources):
    work = np.copy(available)
    finish = [False] * num_processes
    safe_sequence = []
    needs = []

    for p in range(num_processes):
        need = max_need[p] - allocation[p]
        needs.append(need)
    
    while len(safe_sequence) < num_processes:
        allocated_this_round = False
        for p in range(num_processes):
            if not finish[p]:
                need = needs[p]
                if all(need <= work):
                    work += allocation[p]
                    safe_sequence.append(p)
                    finish[p] = True
                    allocated_this_round = True
        if not allocated_this_round:
            return None, needs
    return safe_sequence, needs

st.title("Banker's Algorithm for Hospital Surgery Scheduling")

num_processes = st.number_input('Number of Surgeries', min_value=1, step=1)
num_resources = 4
resources = ['Operation Rooms', 'Surgeons', 'Nurses', 'Medical Equipment']

if num_processes > 0:
    st.subheader("Allocated and Maximum Resources for each Surgery")
    
    cols = st.columns([1, 3, 3])
    cols[0].write("Surgery")
    cols[1].write("Allocated Resources")
    cols[2].write("Maximum Resources")
    
    subcols_alloc = st.columns([1, 1, 1, 1])
    subcols_max = st.columns([1, 1, 1, 1])

    allocated = np.zeros((num_processes, num_resources), dtype=int)
    max_need = np.zeros((num_processes, num_resources), dtype=int)

    for i in range(num_processes):
        st.write(f"-------------------------------------------------------------------------------------------------------------")
        cols = st.columns([1, 3, 3])
        
        cols[0].write(f"Surgery {i + 1}")
        
        allocated[i][0] = cols[1].number_input(f'Rooms', min_value=0, key=f'alloc_room_{i}')
        allocated[i][1] = cols[1].number_input(f'Surgeons', min_value=0, key=f'alloc_surg_{i}')
        allocated[i][2] = cols[1].number_input(f'Nurses', min_value=0, key=f'alloc_nurse_{i}')
        allocated[i][3] = cols[1].number_input(f'Equipment', min_value=0, key=f'alloc_equip_{i}')
        
        max_need[i][0] = cols[2].number_input(f'Rooms', min_value=0, key=f'max_room_{i}')
        max_need[i][1] = cols[2].number_input(f'Surgeons', min_value=0, key=f'max_surg_{i}')
        max_need[i][2] = cols[2].number_input(f'Nurses', min_value=0, key=f'max_nurse_{i}')
        max_need[i][3] = cols[2].number_input(f'Equipment', min_value=0, key=f'max_equip_{i}')

    st.subheader("Available Resources")
    available = []
    available.append(st.number_input('Available Operation Rooms', min_value=0))
    available.append(st.number_input('Available Surgeons', min_value=0))
    available.append(st.number_input('Available Nurses', min_value=0))
    available.append(st.number_input('Available Medical Equipment', min_value=0))
    available = np.array(available)

    if st.button('Calculate Safe Sequence'):
        safe_sequence, needs = is_safe(available, max_need, allocated, num_processes, num_resources)
        
        st.subheader("Calculated Needed Resources for Each Surgery")
        for i in range(num_processes):
            st.write(f"Surgery {i + 1} - Needed: {needs[i]}")

        if safe_sequence is None:
            st.error("No safe sequence found. The system is in an unsafe state!")
        else:
            st.success(f"Safe Sequence: {' -> '.join([f'Surgery {p + 1}' for p in safe_sequence])}")