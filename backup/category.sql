PGDMP         2                y            isso     13.2 (Ubuntu 13.2-1.pgdg20.04+1)     13.2 (Ubuntu 13.2-1.pgdg20.04+1)     ^           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            _           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            `           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            a           1262    16384    isso    DATABASE     Y   CREATE DATABASE isso WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'ru_RU.UTF-8';
    DROP DATABASE isso;
                postgres    false                       1259    26346    searchapp_category    TABLE     ?   CREATE TABLE public.searchapp_category (
    id bigint NOT NULL,
    rus_name character varying(16) NOT NULL,
    eng_name character varying(16) NOT NULL
);
 &   DROP TABLE public.searchapp_category;
       public         heap    postgres    false                       1259    26344    searchapp_category_id_seq    SEQUENCE     ?   CREATE SEQUENCE public.searchapp_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.searchapp_category_id_seq;
       public          postgres    false    261            b           0    0    searchapp_category_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.searchapp_category_id_seq OWNED BY public.searchapp_category.id;
          public          postgres    false    260            ?           2604    26349    searchapp_category id    DEFAULT     ~   ALTER TABLE ONLY public.searchapp_category ALTER COLUMN id SET DEFAULT nextval('public.searchapp_category_id_seq'::regclass);
 D   ALTER TABLE public.searchapp_category ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    260    261    261            [          0    26346    searchapp_category 
   TABLE DATA           D   COPY public.searchapp_category (id, rus_name, eng_name) FROM stdin;
    public          postgres    false    261   w       c           0    0    searchapp_category_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.searchapp_category_id_seq', 6, true);
          public          postgres    false    260            ?           2606    26351 *   searchapp_category searchapp_category_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.searchapp_category
    ADD CONSTRAINT searchapp_category_pkey PRIMARY KEY (id);
 T   ALTER TABLE ONLY public.searchapp_category DROP CONSTRAINT searchapp_category_pkey;
       public            postgres    false    261            [   ?   x??;
A???~Oc?h?+??b????0ML?`?u???Fv??^	Odk,!??e?<"\?F???????#?6,t?Ǆ;?~KhIv֕
O7?v???B??J?)??k?>?Akᙋ^.v?r???ܛ????Jp     