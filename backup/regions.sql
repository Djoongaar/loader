PGDMP     6    "                y            es_test_isso     12.6 (Ubuntu 12.6-1.pgdg20.04+1)    12.2 (Ubuntu 12.2-4)     :           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            ;           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            <           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            =           1262    16384    es_test_isso    DATABASE     ~   CREATE DATABASE es_test_isso WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'ru_RU.UTF-8' LC_CTYPE = 'ru_RU.UTF-8';
    DROP DATABASE es_test_isso;
                postgres    false            �            1259    16783    projectsapp_region    TABLE     �   CREATE TABLE public.projectsapp_region (
    id integer NOT NULL,
    name character varying(256) NOT NULL,
    description text NOT NULL,
    area double precision,
    population bigint
);
 &   DROP TABLE public.projectsapp_region;
       public         heap    postgres    false            �            1259    16924    projectsapp_region_id_seq    SEQUENCE     �   CREATE SEQUENCE public.projectsapp_region_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.projectsapp_region_id_seq;
       public          postgres    false    204            >           0    0    projectsapp_region_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.projectsapp_region_id_seq OWNED BY public.projectsapp_region.id;
          public          postgres    false    241            �           2604    17169    projectsapp_region id    DEFAULT     ~   ALTER TABLE ONLY public.projectsapp_region ALTER COLUMN id SET DEFAULT nextval('public.projectsapp_region_id_seq'::regclass);
 D   ALTER TABLE public.projectsapp_region ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    241    204            6          0    16783    projectsapp_region 
   TABLE DATA           U   COPY public.projectsapp_region (id, name, description, area, population) FROM stdin;
    public          postgres    false    204   �       ?           0    0    projectsapp_region_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.projectsapp_region_id_seq', 95, true);
          public          postgres    false    241            �           2606    17031 .   projectsapp_region projectsapp_region_name_key 
   CONSTRAINT     i   ALTER TABLE ONLY public.projectsapp_region
    ADD CONSTRAINT projectsapp_region_name_key UNIQUE (name);
 X   ALTER TABLE ONLY public.projectsapp_region DROP CONSTRAINT projectsapp_region_name_key;
       public            postgres    false    204            �           2606    17033 *   projectsapp_region projectsapp_region_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.projectsapp_region
    ADD CONSTRAINT projectsapp_region_pkey PRIMARY KEY (id);
 T   ALTER TABLE ONLY public.projectsapp_region DROP CONSTRAINT projectsapp_region_pkey;
       public            postgres    false    204            �           1259    17062 %   projectsapp_region_name_8636d95c_like    INDEX     x   CREATE INDEX projectsapp_region_name_8636d95c_like ON public.projectsapp_region USING btree (name varchar_pattern_ops);
 9   DROP INDEX public.projectsapp_region_name_8636d95c_like;
       public            postgres    false    204            6   �  x����n\E����p���]x/"a���� �+`�%��y�>o�W=�%ќ�X+��类�믪Ԩ��v9��.�Ͱ�m6l�?��n�4�Ӷls��R6��9��tu��?�joA�����m��g9��TIA�P���T��k�m�U��������uޮ��a;Q*��Q1c�.���h��^w��IgC�*��.x��٭�j�^�k�\2���:����[;vp����b�\�d,�X����fx��������i��>��	I0^E_]�N缂��|&As1q��u!%�� *��|���m���Q���>뢷��L�~��)�+AH���J��T��NYk�Y�г�������\)�U��&��W��n���N���D׹�
��ƻ�gr}9jk��M��v������,F}�1�I���?r�eK2A��W�#����+��\M�:U�I:ǃ���3>D�� f<�t:$!$I�!�N'H�e12W3ϩ>�uJ�ε��	s�o�dޔĻ�@g����&S�-��DC��j�0���x�.傳�߁R���>☷Ğ�MR�P���xa"ró�MQ�k��r�Tbl��Ix��EJ��D�C�f�顿�Pa���j���X�a���tz���P`k�'�8�YL�>�cZA��Z~�c�|6X�1Q%:B���ʰ��cw	��P�8�Uj.�1�YT*�˕�>�е��Q*J_�R����>�)���3Hu�n��\O2ʆ �T6Z\�wR=��<ҘѷDi�*�>�(�)k� �&-�֪D���}Zw��	7ͷ��	�!���WJ9��)��,ly%'W�UlO��!���w��)�z�*��`u�(�V%��5�0j�Z���y��;d���-��u1�Хt�'�5f��4�Xt��C��pf�G�����ˢM.xΛ��%���D�4g�W6��5�'�k���Q����=�x	bA��C�C!�N�y��RF�'4�Gɵ�I#\�uq1�M�0:g�Z��c�u�:�,LJ,:�Ub<�ڇ;����u���PmFK��ڜ�Oɐ#*���ɢ�-G�>�j/�Dq��SrO�dR�
�aJ�]6�L����k`�v���A����5�rg������@�+�T�2`Hs��j|�馜4ia��3�����'����h'sw�'���~0�0䄴Cn��N�����/�hH|L��N��pW�<lAFf>R��r�ew�j��\���f��FV��+x�c��ޮ��n�?���Y���Ѷ����/�+��Q��94�`KҶ��}����Me����&m��w,Ag��0��2�/ES�#����G���̅V�erN�8�\큢�7+�O8#/ݖw��g3+d�j6)h;������cWF�~�Ma��
�����q��>�t�.!/R��ڱ��WG��?m)�c)!�T��cۦ��6'-p��	l�ښ��>�-W��?t`f(z�Nz5дzXY����.䶧�HCcf�K,����5�X��2"���:��h+���=�:f�������J*63����w����MdI#�ѤGǈ�k��.�Ø�N�MG`G���-E�Q���d�cÑ�~�_��;l�JU����,9ƋC�ȋ�D8����e�r�3��Qr���H�R����I�Lk�?�.     