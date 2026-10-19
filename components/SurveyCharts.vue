<script setup lang="ts">
import survey from '../data/core-team-survey-2026.json'

defineProps<{ kind: 'confidence' | 'interest' }>()
const languages = ['c', 'rust'] as const

function chartAlt(key: 'c' | 'rust' | 'interest') {
  const question = survey.questions[key]
  return `${question.question} ${question.response_count} responses. Counts for ratings 1 through 5: ${question.counts.join(', ')}.`
}
</script>

<template>
  <template v-if="kind === 'confidence'">
    <div class="survey-confidence">
      <figure v-for="language in languages" :key="language" class="card survey-chart">
        <img :src="`/images/core-team-confidence-${language}.svg`" :alt="chartAlt(language)" />
        <figcaption>
          <b>{{ survey.questions[language].rated_4_or_5 }} of {{ survey.questions[language].response_count }}</b>
          rated 4–5 ({{ Math.round(survey.questions[language].rated_4_or_5_percent) }}%)
        </figcaption>
      </figure>
    </div>
  </template>
  <template v-else>
    <div class="survey-interest">
      <figure class="card survey-chart">
        <img src="/images/core-team-rust-interest.svg" :alt="chartAlt('interest')" />
      </figure>
      <div class="card survey-summary">
        <h3>Ratings 4–5</h3>
        <div class="survey-percentage">{{ Math.round(survey.questions.interest.rated_4_or_5_percent) }}%</div>
        <p>{{ survey.questions.interest.rated_4_or_5 }} of {{ survey.questions.interest.response_count }} respondents</p>
      </div>
    </div>
  </template>
</template>
