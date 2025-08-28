<script lang="ts">
  import { onMount } from 'svelte';
  import { user } from '$lib/stores/auth';
  
  let applications = [];
  let loading = true;
  let error = null;

  onMount(async () => {
    // Load applications data - authentication is handled by layout
    await loadApplications();
  });

  async function loadApplications() {
    try {
      loading = true;
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      applications = [
        {
          id: 1,
          company: 'TechCorp Inc.',
          position: 'Senior Frontend Developer',
          status: 'interview',
          appliedDate: '2024-01-15',
          salary: '$90k - $120k',
          location: 'San Francisco, CA'
        },
        {
          id: 2,
          company: 'StartupXYZ',
          position: 'Full Stack Engineer',
          status: 'applied',
          appliedDate: '2024-01-14',
          salary: '$80k - $110k',
          location: 'Remote'
        }
      ];
    } catch (err) {
      error = 'Failed to load applications';
    } finally {
      loading = false;
    }
  }
</script>

<div class="space-y-6">
  <div class="flex justify-between items-center">
    <h1 class="text-2xl font-bold text-gray-900">Applications</h1>
    <button class="btn btn-primary">New Application</button>
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
      {#each applications as application}
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex justify-between items-start">
            <div>
              <h3 class="text-lg font-semibold text-gray-900">{application.position}</h3>
              <p class="text-gray-600">{application.company}</p>
              <p class="text-sm text-gray-500">
                Applied: {application.appliedDate} • {application.location}
              </p>
            </div>
            <div class="flex space-x-2">
              <span class="px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800">
                {application.salary}
              </span>
              <span class="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800">
                {application.status}
              </span>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
