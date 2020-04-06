<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Moodle is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Moodle.  If not, see <http://www.gnu.org/licenses/>.

/**
 * Library of interface functions and constants.
 *
 * @package     mod_teams
 * @copyright   2016 Alexandru Elisei <alexandru.elisei@gmail.com>, David Mudrák <david@moodle.com>
 * @license     http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

defined('MOODLE_INTERNAL') || die();

// $client = new GearmanClient();
// $client->addServer('localhost', 4730);



/**
 * Return if the plugin supports $feature.
 *
 * @param string $feature Constant representing the feature.
 * @return true | null True if the feature is supported, null otherwise.
 */
function teams_supports($feature) {
    switch ($feature) {
        case FEATURE_GRADE_HAS_GRADE:
            return true;
        case FEATURE_MOD_INTRO:
            return true;
        case FEATURE_BACKUP_MOODLE2:
            return true;
        default:
            return null;
    }
}

/**
 * Saves a new instance of the mod_teams into the database.
 *
 * Given an object containing all the necessary data, (defined by the form
 * in mod_form.php) this function will create a new instance and return the id
 * number of the instance.
 *
 * @param object $moduleinstance An object from the form.
 * @param mod_teams_mod_form $mform The form.
 * @return int The id of the newly inserted record.
 */
function teams_add_instance($teams, $mform=null) {
    global $DB, $client;
    
    // get course context
    // $cmid = $teams->coursemodule;
    // $context = context_module::instance($cmid);
    
    // // get enrolled users
    // $enrolled_users = get_enrolled_sql($context);
    // print_object($enrolled_users);
    
    // $command = escapeshellcmd('/Applications/MAMP/htdocs/moodle/mod/teams/test_team_dev.py');
    // shell_exec("gearmand -d");
    // shell_exec($command);
    
    //file_put_contents('php://stderr', print_r($teams->description, TRUE));
    $file_content = $mform->get_file_content('attachment');
    $file_name = $mform->get_new_filename('attachment');
    $senddata = array($teams->name, "None", "mailNickname", $file_content);
    
    $client = new GearmanClient();
    $client->addServer('localhost', 4730);
    
    $_msteamid = $client->doNormal("create_team", json_encode($senddata));

    $teams->timecreated = time();
    $teams->msteamid = $_msteamid;
    //file_put_contents('php://stderr', print_r($teams->msteamid, TRUE));
    file_put_contents('php://stderr', print_r($file_content, TRUE));
    
    $id = $DB->insert_record('teams', $teams);
    //echo $status;
    return $id;
}

/**
 * TO DO: Think about what updates would the user be able to do inside Teams
 * Updates an instance of the mod_teams in the database.
 *
 * Given an object containing all the necessary data (defined in mod_form.php),
 * this function will update an existing instance with new data.
 *
 * @param object $moduleinstance An object from the form in mod_form.php.
 * @param mod_teams_mod_form $mform The form.
 * @return bool True if successful, false otherwise.
 */
function teams_update_instance($moduleinstance, $mform = null) {
    global $DB;

    $client = new GearmanClient();
    $client->addServer('localhost', 4730);

    $new_name = $moduleinstance->name;
    file_put_contents('php://stderr', print_r($new_name, TRUE));

    
    // check if the team exists in the database
    $exists = $DB->get_record('teams', array('id' => $moduleinstance->instance));
    if (!$exists) {
        file_put_contents('php://stderr', print_r("does_not_exists", TRUE));
        return false;
    }
    
    $senddata = array($exists->msteamid, $new_name);
    $_msteamid = $client->doNormal("update_team", json_encode($senddata));
    
    $moduleinstance->timemodified = time();
    $moduleinstance->id = $moduleinstance->instance;
    $moduleinstance->msteamid = $_msteamid;
    file_put_contents('php://stderr', print_r($_msteamid, TRUE));

    return $DB->update_record('teams', $moduleinstance);
}

/**
 * Removes an instance of the mod_teams from the database.
 *
 * @param int $id Id of the module instance.
 * @return bool True if successful, false on failure.
 */
function teams_delete_instance($id) {
    global $DB;
    file_put_contents('php://stderr', print_r("delete", TRUE));
    $exists = $DB->get_record('teams', array('id' => $id));
    
    if (!$exists) {
        file_put_contents('php://stderr', print_r("does_not_exists", TRUE));
        return false;
    }
    //file_put_contents('php://stderr', print_r($exists, TRUE));
    
    $client = new GearmanClient();
    $client->addServer('localhost', 4730);
    $_msteamid = $client->doNormal("archive_nd_delete_team", json_encode($exists->msteamid));
    $DB->delete_records('teams', array('id' => $id));
    return true;
}

/**
 * Is a given scale used by the instance of mod_teams?
 *
 * This function returns if a scale is being used by one mod_teams
 * if it has support for grading and scales.
 *
 * @param int $moduleinstanceid ID of an instance of this module.
 * @param int $scaleid ID of the scale.
 * @return bool True if the scale is used by the given mod_teams instance.
 */
function teams_scale_used($moduleinstanceid, $scaleid) {
    global $DB;

    if ($scaleid && $DB->record_exists('teams', array('id' => $moduleinstanceid, 'grade' => -$scaleid))) {
        return true;
    } else {
        return false;
    }
}

/**
 * Checks if scale is being used by any instance of mod_teams.
 *
 * This is used to find out if scale used anywhere.
 *
 * @param int $scaleid ID of the scale.
 * @return bool True if the scale is used by any mod_teams instance.
 */
function teams_scale_used_anywhere($scaleid) {
    global $DB;

    if ($scaleid and $DB->record_exists('teams', array('grade' => -$scaleid))) {
        return true;
    } else {
        return false;
    }
}

/**
 * Creates or updates grade item for the given mod_teams instance.
 *
 * Needed by {@link grade_update_mod_grades()}.
 *
 * @param stdClass $moduleinstance Instance object with extra cmidnumber and modname property.
 * @param bool $reset Reset grades in the gradebook.
 * @return void.
 */
function teams_grade_item_update($moduleinstance, $reset=false) {
    global $CFG;
    require_once($CFG->libdir.'/gradelib.php');

    $item = array();
    $item['itemname'] = clean_param($moduleinstance->name, PARAM_NOTAGS);
    $item['gradetype'] = GRADE_TYPE_VALUE;

    if ($moduleinstance->grade > 0) {
        $item['gradetype'] = GRADE_TYPE_VALUE;
        $item['grademax']  = $moduleinstance->grade;
        $item['grademin']  = 0;
    } else if ($moduleinstance->grade < 0) {
        $item['gradetype'] = GRADE_TYPE_SCALE;
        $item['scaleid']   = -$moduleinstance->grade;
    } else {
        $item['gradetype'] = GRADE_TYPE_NONE;
    }
    if ($reset) {
        $item['reset'] = true;
    }

    grade_update('/mod/teams', $moduleinstance->course, 'mod', 'mod_teams', $moduleinstance->id, 0, null, $item);
}

/**
 * Delete grade item for given mod_teams instance.
 *
 * @param stdClass $moduleinstance Instance object.
 * @return grade_item.
 */
function teams_grade_item_delete($moduleinstance) {
    global $CFG;
    require_once($CFG->libdir.'/gradelib.php');

    return grade_update('/mod/teams', $moduleinstance->course, 'mod', 'teams',
                        $moduleinstance->id, 0, null, array('deleted' => 1));
}

/**
 * Update mod_teams grades in the gradebook.
 *
 * Needed by {@link grade_update_mod_grades()}.
 *
 * @param stdClass $moduleinstance Instance object with extra cmidnumber and modname property.
 * @param int $userid Update grade of specific user only, 0 means all participants.
 */
function teams_update_grades($moduleinstance, $userid = 0) {
    global $CFG, $DB;
    require_once($CFG->libdir.'/gradelib.php');

    // Populate array of grade objects indexed by userid.
    $grades = array();
    grade_update('/mod/teams', $moduleinstance->course, 'mod', 'mod_teams', $moduleinstance->id, 0, $grades);
}

/**
 * Returns the lists of all browsable file areas within the given module context.
 *
 * The file area 'intro' for the activity introduction field is added automatically
 * by {@link file_browser::get_file_info_context_module()}.
 *
 * @package     mod_teams
 * @category    files
 *
 * @param stdClass $course.
 * @param stdClass $cm.
 * @param stdClass $context.
 * @return string[].
 */
function teams_get_file_areas($course, $cm, $context) {
    return array();
}

/**
 * File browsing support for mod_teams file areas.
 *
 * @package     mod_teams
 * @category    files
 *
 * @param file_browser $browser.
 * @param array $areas.
 * @param stdClass $course.
 * @param stdClass $cm.
 * @param stdClass $context.
 * @param string $filearea.
 * @param int $itemid.
 * @param string $filepath.
 * @param string $filename.
 * @return file_info Instance or null if not found.
 */
function teams_get_file_info($browser, $areas, $course, $cm, $context, $filearea, $itemid, $filepath, $filename) {
    return null;
}

/**
 * Serves the files from the mod_teams file areas.
 *
 * @package     mod_teams
 * @category    files
 *
 * @param stdClass $course The course object.
 * @param stdClass $cm The course module object.
 * @param stdClass $context The mod_teams's context.
 * @param string $filearea The name of the file area.
 * @param array $args Extra arguments (itemid, path).
 * @param bool $forcedownload Whether or not force download.
 * @param array $options Additional options affecting the file serving.
 */
function teams_pluginfile($course, $cm, $context, $filearea, $args, $forcedownload, $options = array()) {
    global $DB, $CFG;

    if ($context->contextlevel != CONTEXT_MODULE) {
        send_file_not_found();
    }

    require_login($course, true, $cm);
    send_file_not_found();
}

/**
 * Extends the global navigation tree by adding mod_teams nodes if there is a relevant content.
 *
 * This can be called by an AJAX request so do not rely on $PAGE as it might not be set up properly.
 *
 * @param navigation_node $teamsnode An object representing the navigation tree node.
 * @param stdClass $course.
 * @param stdClass $module.
 * @param cm_info $cm.
 */
function teams_extend_navigation($teamsnode, $course, $module, $cm) {
}

/**
 * Extends the settings navigation with the mod_teams settings.
 *
 * This function is called when the context for the page is a mod_teams module.
 * This is not called by AJAX so it is safe to rely on the $PAGE.
 *
 * @param settings_navigation $settingsnav {@link settings_navigation}
 * @param navigation_node $teamsnode {@link navigation_node}
 */
function teams_extend_settings_navigation($settingsnav, $teamsnode = null) {
}
