<script lang="ts">
import { writable } from 'svelte/store';
// ATS score calculation
import { onMount } from 'svelte';
import { uploadResume, scrapeJobLink } from '$lib/services/dashboard';
import { getKeywordMatches } from '$lib/services/keywordMatch';

const resume = writable<string | null>(null);
const jobData = writable<string | null>(null);
const matches = writable<string[]>([]);
const notMatches = writable<string[]>([]);
const suggestions = writable<string[]>([]);
const atsScore = writable<number>(0);

let resumeFile: File | null = null;
let jobUrl = '';
let loadingResume = false;
let loadingJob = false;

async function handleResumeUpload() {
    if (!resumeFile) return;
    loadingResume = true;
    const res = await uploadResume(resumeFile);
    resume.set(res.parsed_content);
    loadingResume = false;
    compareKeywords();
}

async function handleJobScrape() {
    if (!jobUrl) return;
    loadingJob = true;
    const job = await scrapeJobLink(jobUrl);
    jobData.set(job.description);
    loadingJob = false;
    compareKeywords();
}

function compareKeywords() {
    let resumeText: string | null;
    let jobText: string | null;
    resume.subscribe(val => resumeText = val)();
    jobData.subscribe(val => jobText = val)();
    if (resumeText && jobText) {
        const result = getKeywordMatches(resumeText, jobText);
        matches.set(result.matches);
        notMatches.set(result.notMatches);
        suggestions.set(result.suggestions);
        // ATS score: percent of job keywords matched
        const total = result.matches.length + result.notMatches.length;
        atsScore.set(total > 0 ? Math.round((result.matches.length / total) * 100) : 0);
    }
}

function handleFileChange(e) {
    const input = e.target;
    resumeFile = input.files && input.files[0] ? input.files[0] : null;
}
</script>

<header class="w-full bg-gray-100 py-4 px-8 flex items-center justify-between mb-8">
    <h1 class="text-2xl font-bold">Resume & Job Match</h1>
    <a href="/match" class="text-blue-600 hover:underline">Go to Match Page</a>
</header>

<div class="grid grid-cols-2 gap-8 p-8">
    <div class="border rounded-lg p-6 bg-white shadow">
        <h2 class="text-xl font-bold mb-4">Resume Upload</h2>
        <input type="file" accept=".pdf,.docx" on:change={handleFileChange} />
        <button class="mt-2 px-4 py-2 bg-blue-600 text-white rounded" on:click={handleResumeUpload} disabled={loadingResume}>
            {loadingResume ? 'Uploading...' : 'Upload & Parse'}
        </button>
        <div class="mt-4">
            <h3 class="font-semibold">Parsed Resume:</h3>
            {#if $resume}
                <div class="mb-2 text-lg font-bold text-primary-700">ATS Score: {$atsScore}%</div>
                <pre class="bg-gray-100 p-2 rounded whitespace-pre-wrap">{$resume}</pre>
            {:else}
                <div class="text-gray-400 italic">No resume uploaded yet.</div>
            {/if}
        </div>
    </div>
    <div class="border rounded-lg p-6 bg-white shadow">
        <h2 class="text-xl font-bold mb-4">Job Link Processing</h2>
        <input type="text" placeholder="Paste job link here" bind:value={jobUrl} class="w-full border p-2 rounded" />
        <button class="mt-2 px-4 py-2 bg-green-600 text-white rounded" on:click={handleJobScrape} disabled={loadingJob}>
            {loadingJob ? 'Scraping...' : 'Scrape Job'}
        </button>
        <div class="mt-4">
            <h3 class="font-semibold">Job Description:</h3>
            {#if $jobData}
                <pre class="bg-gray-100 p-2 rounded whitespace-pre-wrap">{$jobData}</pre>
            {:else}
                <div class="text-gray-400 italic">No job description scraped yet.</div>
            {/if}
        </div>
    </div>
</div>

{#if $resume && $jobData}
    <div class="mt-8 p-8 bg-white rounded shadow">
        <h2 class="text-xl font-bold mb-4">Keyword Analysis</h2>
        <div class="grid grid-cols-2 gap-8">
            <div>
                <h3 class="font-semibold text-green-700">Matched Keywords</h3>
                <ul class="list-disc ml-6">
                    {#each $matches as word}
                        <li>{word}</li>
                    {/each}
                </ul>
            </div>
            <div>
                <h3 class="font-semibold text-red-700">Unmatched Keywords</h3>
                <ul class="list-disc ml-6">
                    {#each $notMatches as word}
                        <li>{word}</li>
                    {/each}
                </ul>
            </div>
        </div>
        {#if $suggestions.length}
        <div class="mt-6">
            <h3 class="font-semibold text-blue-700">Suggestions</h3>
            <ul class="list-disc ml-6">
                {#each $suggestions as suggestion}
                    <li>{suggestion}</li>
                {/each}
            </ul>
        </div>
        {/if}
    </div>
{/if}
