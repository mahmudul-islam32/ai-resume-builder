<script lang="ts">
  import { onMount } from 'svelte';
  import { user } from '$lib/stores/auth';
  
  let resumes = [];
  let loading = true;
  let error = null;

  onMount(async () => {
    // Load resumes data - authentication is handled by layout
    await loadResumes();
  });

  async function loadResumes() {
    try {
      loading = true;
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      resumes = [
        {
          id: 1,
          name: 'Senior Developer Resume',
          lastUpdated: '2024-01-15',
          status: 'active'
        },
        {
          id: 2,
          name: 'Frontend Developer Resume',
          lastUpdated: '2024-01-10',
          status: 'draft'
        }
      ];
    } catch (err) {
      error = 'Failed to load resumes';
    } finally {
      loading = false;
    }
  }
</script>

<div class="space-y-6">
  <div class="flex justify-between items-center">
    <h1 class="text-2xl font-bold text-gray-900">Resumes</h1>
    <button class="btn btn-primary">Create Resume</button>
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
      {#each resumes as resume}
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex justify-between items-start">
            <div>
              <h3 class="text-lg font-semibold text-gray-900">{resume.name}</h3>
              <p class="text-sm text-gray-500">
                Last updated: {resume.lastUpdated}
              </p>
            </div>
            <div class="flex space-x-2">
              <span class="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800">
                {resume.status}
              </span>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
