<!-- Copyright 2020 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div>
    <div class="row">
      <div class="col-md-6 mb-2 mb-md-0">
        <button type="button" class="btn btn-sm btn-light" :disabled="!showDiff" @click="toggleComparison">
          <i class="fa-solid fa-repeat"></i>
          <span v-if="compareLatest_">{{ $t('Compare to previous revision') }}</span>
          <span v-else>{{ $t('Compare to latest revision') }}</span>
        </button>
      </div>
      <div class="col-md-6 d-md-flex justify-content-end">
        <div>
          <button type="button" class="btn btn-sm btn-light" @click="toggleDiff">
            <span v-if="showDiff">
              <i class="fa-solid fa-eye"></i> {{ $t('Show current revision') }}
            </span>
            <span v-else>
              <i class="fa-solid fa-code-compare"></i> {{ $t('Show changes') }}
            </span>
          </button>
        </div>
      </div>
    </div>
    <hr>
    <div v-if="showDiff">
      <i class="fa-solid fa-circle-info"></i>
      <small>
        <strong v-if="compareLatest_">{{ $t('Comparing to latest revision') }}</strong>
        <strong v-else>{{ $t('Comparing to previous revision') }}</strong>
      </small>
      <hr>
    </div>
    <div v-if="!loading">
      <!-- If we don't have a link to the object itself, we probably don't care about the ID anyways. -->
      <div class="row mb-2" v-if="revision._links.view_object">
        <span class="col-md-3">{{ $t('Object ID') }}</span>
        <a class="col-md-9" :href="revision._links.view_object">
          <strong>{{ revision.object_id }}</strong>
        </a>
      </div>
      <div class="row mt-2">
        <span class="col-md-3">{{ $t('User') }}</span>
        <identity-popover class="col-md-9" :user="revision.revision.user"></identity-popover>
      </div>
      <div class="row mt-2">
        <span class="col-md-3">{{ $t('Timestamp') }}</span>
        <div class="col-md-9">
          <local-timestamp :timestamp="revision.revision.timestamp"></local-timestamp>
          <br>
          <small class="text-muted">
            (<from-now :timestamp="revision.revision.timestamp"></from-now>)
          </small>
        </div>
      </div>
      <hr>
      <div v-for="(value, prop, revisionIndex) in revision.data" :key="prop">
        <div class="row">
          <div class="col-md-3">
            <strong>{{ revisionProp(prop) }}</strong>
          </div>
          <div class="col-md-9 bg-light rounded">
            <pre class="mb-0" v-if="showDiff"><!--
           --><div v-for="(part, partIndex) in getDiff(revision, prop)"
                   :class="{'font-italic': part.value === null}"
                   :key="partIndex"><!--
             --><span class="mb-0 diff-add" v-if="part.added">{{ revisionValue(part.value) }}</span><!--
             --><span class="mb-0 diff-delete" v-else-if="part.removed">{{ revisionValue(part.value) }}</span><!--
             --><span class="mb-0" v-else>{{ revisionValue(part.value) }}</span><!--
           --></div><!--
         --></pre>
            <pre class="mb-0" :class="{'font-italic': value === null}" v-else>{{ revisionValue(value) }}</pre>
          </div>
        </div>
        <br v-if="revisionIndex < Object.keys(revision.data).length - 1">
      </div>
    </div>
    <i class="fa-solid fa-circle-notch fa-spin" v-if="loading"></i>
  </div>
</template>

<style scoped>
pre {
  font-size: 90%;
}

.diff-add {
  color: #009933;
}

.diff-delete {
  color: #ff0000;
}
</style>

<script>
import {diffJson} from 'diff';

export default {
  data() {
    return {
      revision: null,
      loading: true,
      showDiff: true,
      compareLatest_: this.compareLatest,
    };
  },
  props: {
    endpoint: String,
    latestRevision: Number,
    compareLatest: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    revisionProp(prop) {
      return kadi.utils.capitalize(prop).split('_').join(' ');
    },
    revisionValue(value) {
      return value === null ? 'null' : value;
    },
    getDiff(revision, prop) {
      const diff = revision.diff[prop];

      if (diff) {
        // As the null values are converted into strings when using 'diffJson', we handle these cases separately instead
        // in order to visualize null values differently in the DOM.
        if (diff.prev === null) {
          return [{removed: true, value: null}, {added: true, value: diff.new}];
        } else if (diff.new === null) {
          return [{removed: true, value: diff.prev}, {added: true, value: null}];
        }

        return diffJson(diff.prev, diff.new);
      }

      return [{value: revision.data[prop]}];
    },
    loadRevision() {
      this.loading = true;

      const config = {};
      if (this.compareLatest_ && this.latestRevision) {
        config.params = {revision: this.latestRevision};
      }

      axios.get(this.endpoint, config)
        .then((response) => {
          this.revision = response.data;
          this.loading = false;
        })
        .catch((error) => kadi.alerts.danger($t('Error loading revision.'), {request: error.request}));
    },
    toggleComparison() {
      this.compareLatest_ = !this.compareLatest_;
      this.loadRevision();
    },
    toggleDiff() {
      this.showDiff = !this.showDiff;
    },
  },
  mounted() {
    this.loadRevision();
  },
};
</script>
