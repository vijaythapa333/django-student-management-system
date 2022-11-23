create table auth_group
(
    id   INTEGER      not null primary key auto_increment,
    name varchar(150) not null
        unique
);

create table django_content_type
(
    id        INTEGER      not null primary key auto_increment,
    app_label varchar(100) not null,
    model     varchar(100) not null
);

create table auth_permission
(
    id              INTEGER      not null
        primary key auto_increment,
    content_type_id INTEGER      not null
        references django_content_type
            ,
    codename        varchar(100) not null,
    name            varchar(255) not null
);

create table auth_group_permissions
(
    id            INTEGER not null
        primary key auto_increment,
    group_id      INTEGER not null
        references auth_group
            ,
    permission_id INTEGER not null
        references auth_permission
            
);

create index auth_group_permissions_group_id_b120cbf9
    on auth_group_permissions (group_id);

create unique index auth_group_permissions_group_id_permission_id_0cd325b0_uniq
    on auth_group_permissions (group_id, permission_id);

create index auth_group_permissions_permission_id_84c5c92e
    on auth_group_permissions (permission_id);

create index auth_permission_content_type_id_2f476e4b
    on auth_permission (content_type_id);

create unique index auth_permission_content_type_id_codename_01ab375a_uniq
    on auth_permission (content_type_id, codename);

create unique index django_content_type_app_label_model_76bd3d3b_uniq
    on django_content_type (app_label, model);

create table django_migrations
(
    id      INTEGER      not null
        primary key auto_increment,
    app     varchar(255) not null,
    name    varchar(255) not null,
    applied datetime     not null
);

create table django_session
(
    session_key  varchar(40) not null
        primary key,
    session_data TEXT        not null,
    expire_date  datetime    not null
);

create index django_session_expire_date_a5c62663
    on django_session (expire_date);

create table student_management_app_courses
(
    id          INTEGER      not null
        primary key auto_increment,
    course_name varchar(255) not null,
    created_at  datetime     not null,
    updated_at  datetime     not null
);

create table student_management_app_customuser
(
    id           INTEGER      not null
        primary key auto_increment,
    password     varchar(128) not null,
    last_login   datetime,
    is_superuser bool         not null,
    username     varchar(150) not null
        unique,
    first_name   varchar(30)  not null,
    last_name    varchar(150) not null,
    email        varchar(254) not null,
    is_staff     bool         not null,
    is_active    bool         not null,
    date_joined  datetime     not null,
    user_type    varchar(10)  not null
);

create table django_admin_log
(
    id              INTEGER           not null
        primary key auto_increment,
    action_time     datetime          not null,
    object_id       TEXT,
    object_repr     varchar(200)      not null,
    change_message  TEXT              not null,
    content_type_id INTEGER
        references django_content_type
            ,
    user_id         INTEGER           not null
        references student_management_app_customuser
            ,
    action_flag     smallint unsigned not null,
    check ("action_flag" >= 0)
);

create index django_admin_log_content_type_id_c4bce8eb
    on django_admin_log (content_type_id);

create index django_admin_log_user_id_c564eba6
    on django_admin_log (user_id);

create table student_management_app_adminhod
(
    id         INTEGER  not null
        primary key auto_increment,
    created_at datetime not null,
    updated_at datetime not null,
    admin_id   INTEGER  not null
        unique
        references student_management_app_customuser
            
);

create table student_management_app_customuser_groups
(
    id            INTEGER not null
        primary key auto_increment,
    customuser_id INTEGER not null
        references student_management_app_customuser
            ,
    group_id      INTEGER not null
        references auth_group
            
);

create index student_management_app_customuser_groups_customuser_id_1e347552
    on student_management_app_customuser_groups (customuser_id);

create unique index customuser_groups_customuser_id_group_id_d872a780_uniq
    on student_management_app_customuser_groups (customuser_id, group_id);

create index student_management_app_customuser_groups_group_id_61accfd6
    on student_management_app_customuser_groups (group_id);

create table student_management_app_customuser_user_permissions
(
    id            INTEGER not null
        primary key auto_increment,
    customuser_id INTEGER not null
        references student_management_app_customuser
            ,
    permission_id INTEGER not null
        references auth_permission
            
);

create index customuser_user_permissions_customuser_id_41a474d7
    on student_management_app_customuser_user_permissions (customuser_id);

create unique index permissions_customuser_id_permission_id_af9a6989_uniq
    on student_management_app_customuser_user_permissions (customuser_id, permission_id);

create index customuser_user_permissions_permission_id_cd344297
    on student_management_app_customuser_user_permissions (permission_id);

create table student_management_app_sessionyearmodel
(
    id                 INTEGER not null
        primary key auto_increment,
    session_start_year date    not null,
    session_end_year   date    not null
);

create table student_management_app_staffs
(
    id         INTEGER  not null
        primary key auto_increment,
    address    TEXT     not null,
    created_at datetime not null,
    updated_at datetime not null,
    admin_id   INTEGER  not null
        unique
        references student_management_app_customuser
            
);

create table student_management_app_feedbackstaffs
(
    id             INTEGER  not null
        primary key auto_increment,
    feedback       TEXT     not null,
    feedback_reply TEXT     not null,
    created_at     datetime not null,
    updated_at     datetime not null,
    staff_id_id    INTEGER  not null
        references student_management_app_staffs
            
);

create index student_management_app_feedbackstaffs_staff_id_id_6f22a616
    on student_management_app_feedbackstaffs (staff_id_id);

create table student_management_app_leavereportstaff
(
    id            INTEGER      not null
        primary key auto_increment,
    leave_date    varchar(255) not null,
    leave_message TEXT         not null,
    created_at    datetime     not null,
    updated_at    datetime     not null,
    staff_id_id   INTEGER      not null
        references student_management_app_staffs
            ,
    leave_status  INTEGER      not null
);

create index student_management_app_leavereportstaff_staff_id_id_c7710cd5
    on student_management_app_leavereportstaff (staff_id_id);

create table student_management_app_notificationstaffs
(
    id           INTEGER  not null
        primary key auto_increment,
    message      TEXT     not null,
    created_at   datetime not null,
    updated_at   datetime not null,
    stafff_id_id INTEGER  not null
        references student_management_app_staffs
            
);

create index student_management_app_notificationstaffs_stafff_id_id_e69db87c
    on student_management_app_notificationstaffs (stafff_id_id);

create table student_management_app_students
(
    id                 INTEGER      not null
        primary key auto_increment,
    gender             varchar(50)  not null,
    profile_pic        varchar(100) not null,
    address            TEXT         not null,
    created_at         datetime     not null,
    updated_at         datetime     not null,
    admin_id           INTEGER      not null
        unique
        references student_management_app_customuser
            ,
    course_id_id       INTEGER      not null
        references student_management_app_courses
            ,
    session_year_id_id INTEGER      not null
        references student_management_app_sessionyearmodel
            
);

create table student_management_app_feedbackstudent
(
    id             INTEGER  not null
        primary key auto_increment,
    feedback       TEXT     not null,
    feedback_reply TEXT     not null,
    created_at     datetime not null,
    updated_at     datetime not null,
    student_id_id  INTEGER  not null
        references student_management_app_students
            
);

create index student_management_app_feedbackstudent_student_id_id_099e23ad
    on student_management_app_feedbackstudent (student_id_id);

create table student_management_app_leavereportstudent
(
    id            INTEGER      not null
        primary key auto_increment,
    leave_date    varchar(255) not null,
    leave_message TEXT         not null,
    created_at    datetime     not null,
    updated_at    datetime     not null,
    student_id_id INTEGER      not null
        references student_management_app_students
            ,
    leave_status  INTEGER      not null
);

create index student_management_app_leavereportstudent_student_id_id_9ea5372c
    on student_management_app_leavereportstudent (student_id_id);

create table student_management_app_notificationstudent
(
    id            INTEGER  not null
        primary key auto_increment,
    message       TEXT     not null,
    created_at    datetime not null,
    updated_at    datetime not null,
    student_id_id INTEGER  not null
        references student_management_app_students
            
);

create index notificationstudent_student_id_id_f8c05ed7
    on student_management_app_notificationstudent (student_id_id);

create index student_management_app_students_course_id_id_fcd09bed
    on student_management_app_students (course_id_id);

create index student_management_app_students_session_year_id_id_594fc55d
    on student_management_app_students (session_year_id_id);

create table student_management_app_subjects
(
    id           INTEGER      not null
        primary key auto_increment,
    subject_name varchar(255) not null,
    created_at   datetime     not null,
    updated_at   datetime     not null,
    course_id_id INTEGER      not null
        references student_management_app_courses
            ,
    staff_id_id  INTEGER      not null
        references student_management_app_customuser
            
);

create table student_management_app_attendance
(
    id                 INTEGER  not null
        primary key auto_increment,
    created_at         datetime not null,
    updated_at         datetime not null,
    session_year_id_id INTEGER  not null
        references student_management_app_sessionyearmodel
            ,
    subject_id_id      INTEGER  not null
        references student_management_app_subjects
            ,
    attendance_date    date     not null
);

create index student_management_app_attendance_session_year_id_id_0d30545d
    on student_management_app_attendance (session_year_id_id);

create index student_management_app_attendance_subject_id_id_9ae82fd0
    on student_management_app_attendance (subject_id_id);

create table student_management_app_attendancereport
(
    id               INTEGER  not null
        primary key auto_increment,
    status           bool     not null,
    created_at       datetime not null,
    updated_at       datetime not null,
    attendance_id_id INTEGER  not null
        references student_management_app_attendance
            ,
    student_id_id    INTEGER  not null
        references student_management_app_students
            
);

create index attendancereport_attendance_id_id_f765f2a1
    on student_management_app_attendancereport (attendance_id_id);

create index student_management_app_attendancereport_student_id_id_5a58ceea
    on student_management_app_attendancereport (student_id_id);

create table student_management_app_studentresult
(
    id                       INTEGER  not null
        primary key auto_increment,
    subject_exam_marks       REAL     not null,
    subject_assignment_marks REAL     not null,
    created_at               datetime not null,
    updated_at               datetime not null,
    student_id_id            INTEGER  not null
        references student_management_app_students
            ,
    subject_id_id            INTEGER  not null
        references student_management_app_subjects
            
);

create index student_management_app_studentresult_student_id_id_f6cc67b8
    on student_management_app_studentresult (student_id_id);

create index student_management_app_studentresult_subject_id_id_1f0cd017
    on student_management_app_studentresult (subject_id_id);

create index student_management_app_subjects_course_id_id_342668dd
    on student_management_app_subjects (course_id_id);

create index student_management_app_subjects_staff_id_id_5f47119a
    on student_management_app_subjects (staff_id_id);