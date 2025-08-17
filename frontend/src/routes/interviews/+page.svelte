<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { user } from '$lib/stores/auth';
  import type { Interview } from '$lib/types/dashboard';
  import { DateUtils } from '$lib/utils/date';
  
  let interviews: Interview[] = [];
  let loading = true;
  let error: string | null = null;
  let selectedFilter: string = 'upcoming';
  
  const filterOptions = [
    { value: 'upcoming', label: 'Upcoming' },
    { value: 'completed', label: 'Completed' },
    { value: 'all', label: 'All Interviews' }
  ];
  
  onMount(async () => {
    if (!$user) {
      goto('/login');
      return;
    }
    
    await loadInterviews();
  });
  
  async function loadInterviews(): Promise<void> {
    try {
      loading = true;
      error = null;
      
      // Mock data for now
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      interviews = [
        {
          id: '1',
          company_name: 'TechCorp Inc.',
          job_title: 'Senior Frontend Developer',
          interview_date: '2024-01-20T14:00:00Z',
          interview_type: 'video',
          status: 'scheduled',
          notes: 'Technical interview focusing on React and TypeScript'
        },
        {
          id: '2',
          company_name: 'Innovation Labs',
          job_title: 'UI/UX Developer',
          interview_date: '2024-01-22T10:30:00Z',
          interview_type: 'phone',
          status: 'scheduled',
          notes: 'Initial screening call with HR'
        },
        {
          id: '3',
          company_name: 'StartupXYZ',
          job_title: 'Full Stack Engineer',
          interview_date: '2024-01-18T09:00:00Z',
          interview_type: 'in-person',
          status: 'completed',
          notes: 'Went well, discussed project experience'
        },
        {
          id: '4',
          company_name: 'CloudTech Corp',
          job_title: 'Frontend Engineer',
          interview_date: '2024-01-25T15:30:00Z',
          interview_type: 'technical',
          status: 'scheduled',
          notes: 'Coding challenge and system design'
        }
      ];
    } catch (err) {
      error = 'Failed to load interviews';
      console.error('Error loading interviews:', err);
    } finally {
      loading = false;
    }
  }
  
  function getStatusColor(status: string): string {
    switch (status) {
      case 'scheduled': return 'bg-green-100 text-green-800';
      case 'completed': return 'bg-blue-100 text-blue-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  }
  
  function getInterviewTypeIcon(type: string): string {
    switch (type) {
      case 'video': return 'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z';
      case 'phone': return 'M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z';
      case 'in-person': return 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4';
      case 'technical': return 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z';
      default: return 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z';
    }
  }
  
  function handleEdit(interviewId: string): void {
    goto(`/interviews/${interviewId}/edit`);
  }
  
  async function handleDelete(interviewId: string): Promise<void> {
    if (!confirm('Are you sure you want to delete this interview?')) {
      return;
    }
    
    try {
      interviews = interviews.filter(interview => interview.id !== interviewId);
    } catch (err) {
      error = 'Failed to delete interview';
    }
  }
  
  function isUpcoming(interviewDate: string): boolean {
    return new Date(interviewDate) > new Date();
  }
  
  $: filteredInterviews = (() => {
    switch (selectedFilter) {
      case 'upcoming':
        return interviews.filter(interview => isUpcoming(interview.interview_date));
      case 'completed':
        return interviews.filter(interview => !isUpcoming(interview.interview_date) || interview.status === 'completed');
      case 'all':
        return interviews;
      default:
        return interviews;
    }
  })();
</script>

<svelte:head>
  <title>Interviews - AI Resume Builder</title>
</svelte:head>

<div class="px-4 sm:px-6 lg:px-8">
  <!-- Header -->
  <div class="sm:flex sm:items-center">
    <div class="sm:flex-auto">
      <h1 class="text-3xl font-bold text-gray-900">Interview Schedule</h1>
      <p class="mt-2 text-gray-700">
        Manage your interview schedule and preparation notes.
      </p>
    </div>
    <div class="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
      <a href="/interviews/new" class="btn btn-primary">
        Schedule Interview
      </a>
    </div>
  </div>

  <!-- Filters -->
  <div class="mt-6">
    <div class="sm:flex sm:items-center">
      <div class="sm:flex-auto">
        <label for="filter" class="block text-sm font-medium text-gray-700">
          Filter interviews
        </label>
        <select
          id="filter"
          bind:value={selectedFilter}
          class="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-primary-500 focus:outline-none focus:ring-primary-500 sm:text-sm"
        >
          {#each filterOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>
    </div>
  </div>

  {#if error}
    <div class="mt-6 bg-red-50 border border-red-200 rounded-md p-4">
      <div class="flex">
        <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div class="ml-3">
          <p class="text-sm text-red-800">{error}</p>
        </div>
      </div>
    </div>
  {/if}

  {#if loading}
    <div class="mt-8 flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      <span class="ml-3 text-gray-600">Loading interviews...</span>
    </div>
  {:else if filteredInterviews.length === 0}
    <div class="mt-8 text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No interviews found</h3>
      <p class="mt-1 text-sm text-gray-500">
        {selectedFilter === 'all' ? 'Start by scheduling your first interview.' : `No ${selectedFilter} interviews.`}
      </p>
      <div class="mt-6">
        <a href="/interviews/new" class="btn btn-primary">
          Schedule Interview
        </a>
      </div>
    </div>
  {:else}
    <!-- Interviews Grid -->
    <div class="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {#each filteredInterviews as interview}
        <div class="bg-white overflow-hidden shadow rounded-lg border border-gray-200">
          <div class="p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={getInterviewTypeIcon(interview.interview_type)} />
                  </svg>
                </div>
              </div>
              <div class="ml-4 flex-1">
                <div class="flex items-center justify-between">
                  <h3 class="text-lg font-medium text-gray-900 truncate">
                    {interview.job_title}
                  </h3>
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {getStatusColor(interview.status)}">
                    {interview.status}
                  </span>
                </div>
                <p class="text-sm text-gray-600">{interview.company_name}</p>
              </div>
            </div>
            
            <div class="mt-4">
              <div class="flex items-center text-sm text-gray-600">
                <svg class="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {DateUtils.formatDateTime(interview.interview_date)}
              </div>
              
              <div class="flex items-center mt-1 text-sm text-gray-600">
                <svg class="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={getInterviewTypeIcon(interview.interview_type)} />
                </svg>
                {interview.interview_type} interview
              </div>
              
              {#if interview.notes}
                <div class="mt-3">
                  <p class="text-sm text-gray-600 line-clamp-2">
                    {interview.notes}
                  </p>
                </div>
              {/if}
            </div>
          </div>
          
          <div class="bg-gray-50 px-6 py-3">
            <div class="flex items-center justify-between">
              <button
                on:click={() => handleEdit(interview.id)}
                class="text-primary-600 hover:text-primary-700 text-sm font-medium"
              >
                Edit
              </button>
              <button
                on:click={() => handleDelete(interview.id)}
                class="text-red-600 hover:text-red-700 text-sm font-medium"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
