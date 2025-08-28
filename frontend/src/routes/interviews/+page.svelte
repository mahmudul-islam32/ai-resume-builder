<script lang="ts">
  import { onMount } from 'svelte';
  import { user } from '$lib/stores/auth';
  
  let interviews = [];
  let loading = true;
  let error = null;
  let selectedFilter = 'upcoming';
  
  const filterOptions = [
    { value: 'upcoming', label: 'Upcoming' },
    { value: 'completed', label: 'Completed' },
    { value: 'all', label: 'All Interviews' }
  ];

  onMount(async () => {
    // Load interviews data - authentication is handled by layout
    await loadInterviews();
  });

  async function loadInterviews() {
    try {
      loading = true;
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      interviews = [
        {
          id: 1,
          company: 'TechCorp Inc.',
          position: 'Senior Frontend Developer',
          date: '2024-01-20T14:00:00Z',
          type: 'video',
          status: 'scheduled'
        },
        {
          id: 2,
          company: 'Innovation Labs',
          position: 'UI/UX Developer',
          date: '2024-01-22T10:30:00Z',
          type: 'phone',
          status: 'scheduled'
        }
      ];
    } catch (err) {
      error = 'Failed to load interviews';
    } finally {
      loading = false;
    }
  }
</script>

<div class="space-y-6">
  <div class="flex justify-between items-center">
    <h1 class="text-2xl font-bold text-gray-900">Interviews</h1>
    <button class="btn btn-primary">Schedule Interview</button>
  </div>

  {#if loading}
    <div class="flex items-center justify-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>
  {:else if error}
    <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
      {error}
    </div>
  {:else}
    <div class="grid gap-6">
      {#each interviews as interview}
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex justify-between items-start">
            <div>
              <h3 class="text-lg font-semibold text-gray-900">{interview.position}</h3>
              <p class="text-gray-600">{interview.company}</p>
              <p class="text-sm text-gray-500">
                {new Date(interview.date).toLocaleDateString()} at {new Date(interview.date).toLocaleTimeString()}
              </p>
            </div>
            <div class="flex space-x-2">
              <span class="px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800">
                {interview.type}
              </span>
              <span class="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800">
                {interview.status}
              </span>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
