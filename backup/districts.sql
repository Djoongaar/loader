PGDMP         !                y            es_test_isso     12.6 (Ubuntu 12.6-1.pgdg20.04+1)    12.2 (Ubuntu 12.2-4)     @           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            A           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            B           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            C           1262    16384    es_test_isso    DATABASE     ~   CREATE DATABASE es_test_isso WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'ru_RU.UTF-8' LC_CTYPE = 'ru_RU.UTF-8';
    DROP DATABASE es_test_isso;
                postgres    false            ?            1259    16906    projectsapp_district    TABLE     ?   CREATE TABLE public.projectsapp_district (
    id integer NOT NULL,
    title character varying(256) NOT NULL,
    short character varying(256) NOT NULL,
    "full" character varying(256) NOT NULL
);
 (   DROP TABLE public.projectsapp_district;
       public         heap    postgres    false            ?            1259    16912    projectsapp_district_id_seq    SEQUENCE     ?   CREATE SEQUENCE public.projectsapp_district_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.projectsapp_district_id_seq;
       public          postgres    false    236            D           0    0    projectsapp_district_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.projectsapp_district_id_seq OWNED BY public.projectsapp_district.id;
          public          postgres    false    237            ?           2604    17166    projectsapp_district id    DEFAULT     ?   ALTER TABLE ONLY public.projectsapp_district ALTER COLUMN id SET DEFAULT nextval('public.projectsapp_district_id_seq'::regclass);
 F   ALTER TABLE public.projectsapp_district ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    237    236            <          0    16906    projectsapp_district 
   TABLE DATA           H   COPY public.projectsapp_district (id, title, short, "full") FROM stdin;
    public          postgres    false    236   ?       E           0    0    projectsapp_district_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.projectsapp_district_id_seq', 98, true);
          public          postgres    false    237            ?           2606    17019 2   projectsapp_district projectsapp_district_full_key 
   CONSTRAINT     o   ALTER TABLE ONLY public.projectsapp_district
    ADD CONSTRAINT projectsapp_district_full_key UNIQUE ("full");
 \   ALTER TABLE ONLY public.projectsapp_district DROP CONSTRAINT projectsapp_district_full_key;
       public            postgres    false    236            ?           2606    17021 .   projectsapp_district projectsapp_district_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.projectsapp_district
    ADD CONSTRAINT projectsapp_district_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.projectsapp_district DROP CONSTRAINT projectsapp_district_pkey;
       public            postgres    false    236            ?           2606    17023 3   projectsapp_district projectsapp_district_short_key 
   CONSTRAINT     o   ALTER TABLE ONLY public.projectsapp_district
    ADD CONSTRAINT projectsapp_district_short_key UNIQUE (short);
 ]   ALTER TABLE ONLY public.projectsapp_district DROP CONSTRAINT projectsapp_district_short_key;
       public            postgres    false    236            ?           2606    17025 3   projectsapp_district projectsapp_district_title_key 
   CONSTRAINT     o   ALTER TABLE ONLY public.projectsapp_district
    ADD CONSTRAINT projectsapp_district_title_key UNIQUE (title);
 ]   ALTER TABLE ONLY public.projectsapp_district DROP CONSTRAINT projectsapp_district_title_key;
       public            postgres    false    236            ?           1259    17052 '   projectsapp_district_full_755beb59_like    INDEX     ~   CREATE INDEX projectsapp_district_full_755beb59_like ON public.projectsapp_district USING btree ("full" varchar_pattern_ops);
 ;   DROP INDEX public.projectsapp_district_full_755beb59_like;
       public            postgres    false    236            ?           1259    17053 (   projectsapp_district_short_8d45d047_like    INDEX     ~   CREATE INDEX projectsapp_district_short_8d45d047_like ON public.projectsapp_district USING btree (short varchar_pattern_ops);
 <   DROP INDEX public.projectsapp_district_short_8d45d047_like;
       public            postgres    false    236            ?           1259    17054 (   projectsapp_district_title_efd64612_like    INDEX     ~   CREATE INDEX projectsapp_district_title_efd64612_like ON public.projectsapp_district USING btree (title varchar_pattern_ops);
 <   DROP INDEX public.projectsapp_district_title_efd64612_like;
       public            postgres    false    236            <   ?   x???M?0???^@??.?ą???	?Ѹ4???D?9X+F?tA??y?^?5?G?-~!nd?-?^ ?#7h?r??KF??,??b???$?)ڻ?!tv?HƎ??ӝ7Y?p?/Pغ?NRO`??LZ+ד?ӄl^?*?????/???)?17&H?N*$?@`/?{?*???q(?J?ˮ???Z)??GŌNś:??g????u?;4?-?0????     