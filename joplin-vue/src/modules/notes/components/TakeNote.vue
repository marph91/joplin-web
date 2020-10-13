<template>
  <form method="post" class="form-horizontal" @submit.prevent="doNote">
    <b-alert v-if="updated == 1" v-model="updated" variant="success" show>Update done</b-alert>
    <b-alert v-if="updated == 0" v-model="updated" variant="danger">Update failed</b-alert>
    <p v-if="errors.length">
      <b>Please correct the following error(s):</b>
      <b-alert variant="danger" v-for="error in errors" :key="error" show>{{ error }}</b-alert>
    </p>
    <div class="form-group row">
      <div class="input-group input-group-sm mb-3">
        <b-form-input v-model="title"
                      type="text"
                      name="title"
                      id="title"
                      placeholder="Enter your title">
        </b-form-input>
        <div class="input-group-append">
          <div class="mb-1">
            <b-button v-if="id" size="sm" variant="danger" @click="showMsgRemove(id)"><i class="fas fa-trash"></i> Delete this note ?
            </b-button>
          </div>
        </div>
      </div>
    </div>
    <div class="form-group row">
      <div class="col-sm-2">
      <label v-if="is_todo==1" class="btn btn-secondary btn-sm active"><i class="fas fa-tasks"></i> Tasks ?
        <input name="is_todo" id="is_todo" v-model="is_todo" type="checkbox" checked autocomplete="off"/>
      </label>
      <label v-if="is_todo==0" class="btn btn-secondary btn-sm"><i class="fas fa-tasks"></i> Tasks ?
        <input name="is_todo" id="is_todo" v-model="is_todo" type="checkbox" autocomplete="on"/>
      </label>
      </div>
      <div class="col-sm-2">
        <b-btn size="sm" variant="secondary"><i class="fas fa-calendar"></i></b-btn>
        <span v-if="todo_due"> {{ todo_due }}</span>
      </div>
      <div class="col-sm-7">
        <div class="form-group">
          <div class="input-group input-group-sm mb-3">
            <div class="input-group-prepend">
              <label class="input-group-text" for="inputGroupSelect02">
                <i class="fas fa-tag"></i> Tag
              </label>
              <treeselect v-model="tag"
                    :multiple="true"
                    :disable-branch-nodes="true"
                    :options="this.getTreeTags"
                    ref="tagtreeselect"/>
            </div>
          </div>
        </div>
      </div>
      <div class="col-sm-1">
        <div class="input-group-prepend">
          <b-btn id="note-info" size="sm" variant="secondary"><i class="fas fa-info-circle"></i></b-btn>
          <b-popover target="note-info" triggers="hover focus">
            <template slot="title">Note details</template>
            <ul>
              <li v-if="author !== ''">Author: {{ author }}</li>
              <li v-else>Author n/a</li>
              <li v-if="source_url !== ''">URL: <a v-bind:href="source_url" v-bind:title="source_url">Go to the source</a></li>
              <li v-else>URL n/a</li>
              <li>Date
                <ul>
                  <li v-if="created_time > 0">Created: {{ created_time }}</li>
                  <li v-if="updated_time > 0">Updated: {{ updated_time }}</li>
                </ul>
              </li>
              <li>Geo location
                <ul>
                <li>Latitude {{ latitude }}</li>
                <li>Longitude {{ longitude }}</li>
                <li>Altitude {{ altitude }}</li>
                </ul>
              </li>
              <li>Tasks
                <ul>
                  <li v-if="todo_completed > 0">Todo Completed: {{ todo_completed }}</li>
                  <li v-else>Todo Competed: n/a</li>
                  <li v-if="todo_due > 0">Todo Due: {{ todo_due }}</li>
                  <li v-else>Todo Due: n/a</li>
                </ul>
              </li>
              <li>Source
                <ul>
                  <li>Source: {{ source }}</li>
                  <li>Source Application: {{ source_application }}</li>
                  <li>ID: {{ id }}</li>
                </ul>
              </li>
            </ul>
          </b-popover>
        </div>
      </div>
    </div>
    <div class="form-group">
      <div class="input-group input-group-sm mb-3">
        <div class="input-group-prepend">
          <label class="input-group-text" for="inputGroupSelect01"><i class="fas fa-folder-open"></i> Folder</label>
          <treeselect v-model="parent_id"
                :multiple="false"
                :disable-branch-nodes="false"
                :options="this.getTreeFolders"
                ref="treeselect"/>
        </div>
      </div>
    </div>
    <div class="form-group row">
      <div class="col-sm-6">
        <b-form-textarea id="body"
                         v-model="body"
                         placeholder="Enter something"
                         :rows="25"
                         :max-rows="40"
                         @input="updateBody">
        </b-form-textarea>
        <b-alert v-if="updated == 1" v-model="updated" variant="success" show>Update done</b-alert>
        <b-alert v-if="updated == 0" v-model="updated" variant="danger">Update failed</b-alert>
        <button class="btn btn-primary">
          <span><i class="fas fa-save"></i> Save</span>
        </button>
      </div>
      <div class="col-sm-6">
        <div v-html="compiledMarkdown"></div>
      </div>
    </div>
  </form>
</template>

<script>
import axios from 'axios'

import { createNamespacedHelpers } from 'vuex'

import getters from '../getters'
import actions from '../actions'
import types from '../types'

import { createHelpers } from 'vuex-map-fields'

// import the component
import Treeselect from '@riophae/vue-treeselect'
// import the styles
import '@riophae/vue-treeselect/dist/vue-treeselect.css'

import _ from 'lodash'

const namespace = 'notes'
const { mapGetters, mapActions } = createNamespacedHelpers(namespace)

const { mapFields } = createHelpers({
  getterType: 'getNoteField',
  mutationType: 'updateNoteField'
})

// markdown it + hightlight
// https://markdown-it.github.io/markdown-it/
// https://highlightjs.org/
const hljs = require('highlight.js')

// Actual default values
const md = require('markdown-it')({
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return '<pre class="hljs"><code>' +
               hljs.highlight(lang, str, true).value +
               '</code></pre>'
      } catch (__) {}
    }
    return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>'
  }
})
// markdown it + hightlight

export default {

  data () {
    return {
      urlResources: '/files',
      updated: -1,
      folders: [],
      errors: []
    }
  },
  components: { Treeselect },
  methods: {
    doNote (e) {
      this.errors = []

      if (this.parent_id === undefined) {
        this.errors.push('folder required.')
      }
      if (this.body === '' && this.title === '') {
        this.errors.push('You need the fill the title or the body.')
      }

      if (!this.errors.length) {
        if (this.id === undefined || this.id === 0) {
          this.addNote()
        } else {
          this.updateNote()
        }
        return true
      }

      e.preventDefault()
    },
    /* create a note */
    addNote () {
      const payload = {
        title: this.title,
        body: this.body,
        parent_id: this.parent_id,
        is_todo: (this.is_todo ? 1 : 0),
        tag: this.tag
      }
      this.$store.dispatch('notes/' + types.NOTE_CREATE, payload)
    },
    /* update the note */
    updateNote () {
      // payload
      const payload = {
        id: this.id,
        title: this.title,
        body: this.body,
        parent_id: this.parent_id,
        tag: this.tag,
        is_todo: (this.is_todo ? 1 : 0)
      }
      // push the data
      this.$store.dispatch('notes/' + types.NOTE_CHANGE, payload)
        .then((res) => {
          this.updated = 1
        })
        // eslint-disable-next-line
        .catch((error) => {
          this.updated = 0
        })
    },
    // popup to confirm the deletion
    showMsgRemove (id) {
      this.$bvModal.msgBoxConfirm('Please confirm that you want to delete this note.', {
        title: 'Please Confirm',
        size: 'sm',
        buttonSize: 'sm',
        okVariant: 'danger',
        okTitle: 'YES',
        cancelTitle: 'NO',
        footerClass: 'p-2',
        hideHeaderClose: false,
        centered: true
      })
        .then(value => {
          if (value === true) {
            this.removeNote(id)
          }
        })
        .catch(err => {
          // eslint-disable-next-line no-console
          console.log(err)
        })
    },
    /* delete action pressed */
    removeNote (id) {
      this.$store.dispatch('notes/' + types.NOTE_REMOVE, id)
    },
    // translate markdown to html
    updateBody: _.debounce(function (e) {
      // spot image markdown
      // eslint-disable-next-line
      // let re = /\!\[(.*)\.(\w+)\]\(:\/(.*)\)/g
      // eslint-disable-next-line
      let re = /\!\[(.*)\]\(:\/(.*)\)/g
      // image markdown : ![image name.extension](:/resource_id)
      // becomes
      // image markdown : ![image name.extension](http://127.0.0.1:8001/static/resource_id.extension)
      // add the URL to access to the image from the back http service
      // this.body = e.replace(re, '![$1.$2](' + this.urlResources + '/$3.$2)')
      this.body = e.replace(re, '![$1](' + this.urlResources + '/$2)')
      re = /<img(.*)src=":\/(.*)"(.*)\/>/g
      this.body = e.replace(re, '![$2](' + this.urlResources + '/$2$3)')
      this.getImgBody()
    }, 300),
    ...mapActions(Object.keys(actions)),
    getImgBody () {
      const re = /<img(.*)src=":\/(.*)"(.*)\/>/g
      const result = re.exec(this.body)
      if (result !== null) {
        const resourceId = result[2]
        let resourceFile = ''
        axios.get('/api/jw/resources/' + resourceId)
          .then((res) => {
            resourceFile = resourceId + '.' + res.data.file_extension
            const replaceIt = '<img$1src="' + this.urlResources + '/' + resourceFile + '"$3/>'
            this.body = this.body.replace(re, replaceIt)
          })
          .catch(error => {
            // eslint-disable-next-line no-console
            console.log(error.statusText)
          })
      }
    }
  },
  // load the data of the store into the form for each input
  computed: {
    // default mode
    compiledMarkdown: function () {
      let body = ''
      if (this.$store.state.notes.note.body !== undefined) {
        body = this.$store.state.notes.note.body
      }
      const re = /!\[(.*)\.(\w+)\]\(:\/(.*)\)/g
      body = body.replace(re, '![$1.$2](' + this.urlResources + '/$3.$2)')
      this.getImgBody()
      return md.render(body)
    },
    ...mapGetters(Object.keys(getters)),
    ...mapFields('notes', {
      id: 'note.id',
      title: 'note.title',
      body: 'note.body',
      is_todo: 'note.is_todo',
      parent_id: 'note.parent_id',
      created_time: 'note.user_created_time',
      updated_time: 'note.updated_time',
      todo_completed: 'note.todo_completed',
      todo_due: 'note.todo_due',
      source_url: 'note.source_url',
      author: 'note.author',
      latitude: 'note.latitude',
      longitude: 'note.longitude',
      altitude: 'note.altitude',
      source: 'note.source',
      source_application: 'note.source_application'
    }),
    tag: {
      get () {
        const tags = []
        for (const tag in this.$store.state.notes.tag) {
          tags.push(this.$store.state.notes.tag[tag].id)
        }
        return tags
      },
      set () {
      }
    }
  },
  mounted () {
    // trick : put the default value of the selected folder id by using $ref
    // defined as property in the form :P
    if (this.parent_id !== undefined || this.parent_id !== 0) {
      this.$refs.treeselect.$emit('select', this.parent_id)
    }
    if (process.env.NODE_ENV === 'development') {
      this.urlResources = 'http://127.0.0.1:8001/files'
    }
  }
}
</script>
