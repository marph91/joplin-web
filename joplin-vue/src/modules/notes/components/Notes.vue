<template>
  <div>
    <h5 v-html="this.title"></h5>
    <b-btn v-b-toggle.filterAndSearch variant="primary" size="sm"><i class="fas fa-search"></i> Search and Filter</b-btn>
    <b-collapse id="filterAndSearch" class="mt-2">
      <b-form-group
        label="Sort"
        label-cols-sm="3"
        label-size="sm"
        label-for="sortBySelect"
        class="mb-0"
      >
        <b-input-group size="sm">
          <b-form-select v-model="sortBy" id="sortBySelect" :options="sortOptions" class="w-75">
            <template v-slot:first>
              <option value="">-- none --</option>
            </template>
          </b-form-select>
          <b-form-select v-model="sortDesc" size="sm" :disabled="!sortBy" class="w-25">
            <option :value="false">Asc</option>
            <option :value="true">Desc</option>
          </b-form-select>
        </b-input-group>
      </b-form-group>
      <b-form-group
        label="Filter"
        label-cols-sm="3"
        label-size="sm"
        label-for="filterInput"
        class="mb-0"
      >
        <b-input-group size="sm">
          <b-form-input
            v-model="filter"
            type="search"
            id="filterInput"
            placeholder="Type to Search"
          ></b-form-input>
          <b-input-group-append>
            <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
          </b-input-group-append>
        </b-input-group>
      </b-form-group>
    </b-collapse>
    <b-tabs>
      <b-tab title="notes" active>
        <div class="overflow-auto">
            <b-table
              small
              id="my-notes"
              :items='notes'
              :per-page='perPage'
              :current-page='currentPage'
              :fields='fields'
              :filter='filter'
              :sort-by.sync="sortBy"
              :sort-desc.sync="sortDesc"
              @filtered="onFiltered"
            >
              &nbsp;<template v-slot:cell(title)="data">
                <b-link :to="{ name: 'myNote', params: { id: data.item.title } }"
                    replace
                    v-slot="{ href }">
                  <a :href="href" @click="editNote(data.item)">{{ data.item.title }}</a>
                </b-link>
                <tag :parent_folder="Object.assign({}, data.item.tag)"/>
                <div class="text-sm text-muted font-italic" style="font-size: 0.7rem">Created: {{ data.item.created_time }} - Updated: {{ data.item.updated_time }}</div>
              </template>
            </b-table>
            <b-pagination
              v-model="currentPage"
              :total-rows="notes.length"
              :per-page="perPage"
              aria-controls="my-notes"
            ></b-pagination>
          </div>
      </b-tab>
      <b-tab title="tasks">
        <div class="overflow-auto">
            <b-table
              id="my-tasks"
              :items="tasks"
              :per-page="perPage"
              :current-page="currentPageTasks"
              :fields='fields'
              :tbody-tr-class='rowClass'
              small
            >
              &nbsp;<template v-slot:cell(title)="data">
                <b-link :to="{ name: 'myNote', params: { id: data.item.title } }"
                    replace
                    v-slot="{ href }">
                  <a :href="href" @click="editNote(data.item)">{{ data.item.title }}</a>
                </b-link>
                <tag :parent_folder="Object.assign({}, data.item.tag)"/>
                <div v-if="data.item.todo_completed > 0" class="text-sm text-muted font-italic" style="font-size: 0.7rem">Completed: {{ data.item.completed }}</div>
                <div v-if="data.item.todo_due > 0" class="text-sm text-muted font-italic" style="font-size: 0.7rem">Due: {{ data.item.todo_due }}</div>
                <div class="text-sm text-muted font-italic" style="font-size: 0.7rem">Created: {{ data.item.created_time }} - Updated: {{ data.item.updated_time }}</div>
              </template>
            </b-table>
            <b-pagination
              v-model="currentPageTasks"
              :total-rows="tasks.length"
              :per-page="perPage"
              aria-controls="my-tasks"
            ></b-pagination>
          </div>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import { createNamespacedHelpers } from 'vuex'
import { createHelpers } from 'vuex-map-fields'
import getters from '../getters'
import actions from '../actions'
import types from '../types'

import Tag from './Tag'

const namespace = 'notes'
const { mapGetters, mapActions } = createNamespacedHelpers(namespace)

const { mapFields } = createHelpers({
  getterType: 'getNoteField',
  mutationType: 'updateNoteField'
})

export default {
  data () {
    return {
      page: 0,
      currentPage: 1,
      currentPageTasks: 1,
      perPage: 10,
      fields: [
        { key: 'title', label: 'Note', sortable: true }
      ],
      sortBy: 'created_time',
      sortDesc: true,
      filter: '',
      fieldsToSort: [
        { key: 'title', label: 'Title', sortable: true },
        { key: 'created_time', label: 'Created Date', sortable: true },
        { key: 'updated_time', label: 'Updated Date', sortable: true },
        { key: 'todo_due', label: 'Due Date', sortable: true }
      ]
    }
  },
  components: { Tag },
  methods: {
    editNote (note) {
      this.$store.dispatch('notes/' + types.NOTE_SET, note)
      this.$store.dispatch('notes/' + types.NOTETAG_SET, note)
    },
    delNote (id) {
      this.$store.dispatch('notes/' + types.NOTE_REMOVE, id)
    },
    onFiltered (filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length
      this.currentPage = 1
    },
    ...mapActions(Object.keys(actions)),
    rowClass (item, type) {
      if (!item) return
      if (item.todo_completed > 0) return 'table-secondary'
    }
  },
  computed: {
    ...mapGetters(Object.keys(getters)),
    title: {
      get () {
        if (this.$store.state.folders.folder.title !== undefined) {
          return '<i class="fas fa-folder-open"></i> From Folder / ' + this.$store.state.folders.folder.title
        } else if (this.$store.state.tags.tag.title !== undefined) {
          return '<i class="fas fa-tags"></i> From Tag / ' + this.$store.state.tags.tag.title
        }
        return 'All notes'
      }
    },
    /* only get notes that are not "tasks" */
    notes () {
      return this.$store.state.notes.notes.filter(note => note.is_todo === 0)
    },
    /* only get the tasks */
    tasks () {
      return this.$store.state.notes.notes.filter(note => note.is_todo === 1)
    },
    sortOptions () {
      // Create an options list from our fields
      return this.fieldsToSort
        .filter(f => f.sortable)
        .map(f => {
          return { text: f.label, value: f.key }
        })
    },
    ...mapFields('notes', {
      id: 'note.id',
      is_todo: 'note.is_todo',
      parent_id: 'note.parent_id',
      created_time: 'note.user_created_time',
      updated_time: 'note.updated_time',
      todo_completed: 'note.todo_completed',
      todo_due: 'note.todo_due',
      author: 'note.author',
      tag: 'tag.id'
    })
  },
  mounted () {
    this.$store.dispatch('notes/' + types.NOTE_FETCH_ALL)
  }
}
</script>
