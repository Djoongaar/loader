PGDMP         3                y            isso     13.3 (Ubuntu 13.3-1.pgdg20.04+1)     13.3 (Ubuntu 13.3-1.pgdg20.04+1)     `           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            a           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            b           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            c           1262    16384    isso    DATABASE     Y   CREATE DATABASE isso WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'ru_RU.UTF-8';
    DROP DATABASE isso;
                postgres    false            �            1259    26195    searchapp_searchrequest    TABLE     �   CREATE TABLE public.searchapp_searchrequest (
    id bigint NOT NULL,
    origin text NOT NULL,
    lemma text NOT NULL,
    date timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    category character varying(256)
);
 +   DROP TABLE public.searchapp_searchrequest;
       public         heap    postgres    false            �            1259    26193    searchapp_searchrequest_id_seq    SEQUENCE     �   CREATE SEQUENCE public.searchapp_searchrequest_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.searchapp_searchrequest_id_seq;
       public          postgres    false    249            d           0    0    searchapp_searchrequest_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.searchapp_searchrequest_id_seq OWNED BY public.searchapp_searchrequest.id;
          public          postgres    false    248            �           2604    26198    searchapp_searchrequest id    DEFAULT     �   ALTER TABLE ONLY public.searchapp_searchrequest ALTER COLUMN id SET DEFAULT nextval('public.searchapp_searchrequest_id_seq'::regclass);
 I   ALTER TABLE public.searchapp_searchrequest ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    249    248    249            ]          0    26195    searchapp_searchrequest 
   TABLE DATA           ]   COPY public.searchapp_searchrequest (id, origin, lemma, date, user_id, category) FROM stdin;
    public          postgres    false    249   �       e           0    0    searchapp_searchrequest_id_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.searchapp_searchrequest_id_seq', 287, true);
          public          postgres    false    248            �           2606    26203 4   searchapp_searchrequest searchapp_searchrequest_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.searchapp_searchrequest
    ADD CONSTRAINT searchapp_searchrequest_pkey PRIMARY KEY (id);
 ^   ALTER TABLE ONLY public.searchapp_searchrequest DROP CONSTRAINT searchapp_searchrequest_pkey;
       public            postgres    false    249            �           1259    26219 (   searchapp_searchrequest_user_id_ebdd0845    INDEX     o   CREATE INDEX searchapp_searchrequest_user_id_ebdd0845 ON public.searchapp_searchrequest USING btree (user_id);
 <   DROP INDEX public.searchapp_searchrequest_user_id_ebdd0845;
       public            postgres    false    249            �           2606    26214 P   searchapp_searchrequest searchapp_searchrequest_user_id_ebdd0845_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.searchapp_searchrequest
    ADD CONSTRAINT searchapp_searchrequest_user_id_ebdd0845_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.searchapp_searchrequest DROP CONSTRAINT searchapp_searchrequest_user_id_ebdd0845_fk_auth_user_id;
       public          postgres    false    249            ]   =  x��\�n\�]�_1{C��W?�7��&��B�2o��@8�M` �f��Lٲ�3���3�[3�I����!Q��5���f8[�\�Z��d�j���ճ��g7��#£(�0.b^r^��߉t�g�]\^^<=g<[}��Z}��H�_����߭?_�~u��|����2�P`�������y���o�^,.>�|��Ǘ�a�����.Ιn&�.��,Q�@������BK��5gv��L���*	�2=�ȲdD)2�[ƞs�r�R�QB�,�h.�Y�".%L2��_����H�R@���a�g<������X�2�ڪ����贌 #�:F�R]W!�:>
�>�Rs,������ �ƈ҇޲ȥxn�>�u�I��I��P*5q	J{�����B'S��d��B#g���Ւ�~˘祐~-YT?+����~�4�%���OHK��%Vg�wA��,�@A���U�{����>���B����GW	�Ȋ�9;�죫�^5l�cK��誢̜�?�}t�x�Q�XkS���=IL.��}t�TW1Ąj��}tU�U"�r���N�����c;�;�jZ��IM������H(e�C狼ق�R2:K�;�j�xF%&�Νt5[(ϩx\:��
����x�t��b���\���N�Z5	5Jv�Z�,Z�d6����'�ɉ�cF�Tp� 1Ja飞��)F��r8FL�B. c�[��'��z��C��G=R���Kfj�Tt8'rF��QO��j�jq�c����4�1W�7��}\)[	"�!:�;�jYbV����񽏮�rF�^M<z]�V��0  3���CW�J"j"V�:yݒw��H��$X�_8���n�#egf ���jeu�˸!�����#�&����V��Vz������MU&��:����58�0��fJ_{U˯V�w�o�?Y}o��-^�y��/}�G4��@L��O��I	s�,^���Ɖ	T�ϚSBqNY���vm"]�0e�NL� �;�;)���0'��)�yRق1�#�7�0e�OJ�(����?�)~b�j�R\�0�NL�hzI��m��8�d�`�FK�28G��H�������!�5��T�;�,J(d^B ��0��&�1�-t�o��#��w�}t��p�b�����C�;$�P;ȇ�e6H�������� w������A>��A��R��g�������ə
|h� �.:)����Нj.A}�J��^C{���IC1��l"�j�@.@ٝ�%�A0���8�%�A��*�:X�H����)�\"Lv�(�D��\"�f��`r��3s!���	&of��(��>�&54�����h�5u��?�%gVY���h���IH�l#�����N��GJ_V�9�8#��R%�sq$�	_g�<GB��I"�e<GB�F��ӎ��8��WGR��'p��:�-dT3�ct��#1[��"��8(�p$F`iwr�����d��)	�h]&��}J2� }Rњ�"at�0�C}Rەq,����Yx��@�$9#�)�,<�@ �Pr��<�dc�I	��H�&�}m����R	� Х$���'%�f?B.����\<	Z�|���+\�M�'&���j�M���x͙rHV����'�hEL,%�hf����
��R��x�'%��J�Fߊ29spb5���Q��œPk@���9&'NL a M3}�����I	�g,�g;����s-���
�h#;�2�!2�11��4�$M)|�F4�!˧3��]�	�6�f�C�kv��c���.��bt���c��۝hᄾ��c�્zR�,�3�C먵�E��7g=�0Z�����hᕃ���3Uv��cc���L�qC�I����ˉe�Ao���U/����6x�<"b_��1����"6%Vͽ�6Vn:��O>��1�a�h�ћ����v�O��wU=F3xu� ����QY�WGK�szg���G*��d����I�}I�S���� ���z�g|�jF�4z�wR��Ƅ䳘���ȉ�/�1�a�P��a�LN��ަ��:Z�Ik��"9��U=�4xu��ѫ+����钃F ��HMP��(���ہB�Z�Y��Y��9a�����ɉ	�;)��Ox5�F�H���!;�Q#��j$9�'p5+1Y)VM��|�����H�-V�6�����)ȕ�������_��&�-꩔�0ۭ�I�Ρ�,�����[K{�)���SC<��mf1�@$�����vKj��ġ�x��O-Z�"����vj�Z�b�ͱn�S�U|��W�M,Z-��f�u��ܲQ˕���-&ϖt��V��W��_�����b�{�U&�����!;�-��/)�1,�Mv<��	���Y����ۤ��Sz0ƫprU
X���U��Bs[V��ܩ"O-���������`��5�s: �vq<k�[�w��v��U%�J�V�W�.ۭ��ytB�Ƕv��س�UcptJLǶvmk���Z��o����뺵��`N[������W�?x��)�i'm&JvPt ��~��r�� ֟�x�n2lȪ��$R���#���B{�#�#��?�D�
���=��+n+'p�~$Z�}�Z�D}���~̵۔[	��I J^ʏ(�,u5�$ܪ��7Ƕ,�,�E�Q"F�ߞ�m]��U�yk]6�k"۾��I�?c�}���̆�Qs�~�����ӝ��;[ ����I���l��m-�ؚ%d�a��t���D1�d8бc'�m{���Tg���	b�Z4Њ� ���o؆kqN�%\nz�m	�A���/�{�(n=����Y���/�@c>@;�`C��� ��1h,J�6���?P0(
,1��g���q����tE[X9��a�jh��&��QUN��v��b�i�U�tki�,��>��#�8֖,�t�<YG�0��8��Zd�s6[��Sr�݉���.�h�Ў,�rm��ݑu/���"��9��?�l� �*Q!��e��^ie�MD�=U7f-�%��pL�;���Z��D�qR���L<����q�̯����Zq[O�����h�8[�ɠ��Bg��b
셁���'��6�oQW�[g�`�}{#�osP京���_^�{��9Z�ݛ�4Ǣ\�u�v�������F+<&��5��T�#���5a�9�CP�������ًk7Gͨ&�2押b���]�53�$��9�AM�z����,�`�_�z��~��|��f������7!�?nC;.��c;��@���;�/��l�(]*W��֟�q�������/56���#����t��Vb�{뚗��Q2���S�u-���d$�-�&�F�Li�ȋcR}ˤ-���]xdM�oyd<jo�h��L����ą��o�[�w� ����Ή�<�����~�c����S��L7�r`���3�\O�v�{�v��-m/��ۅ"�6}F{\��o�>RJ��x����Vh!|1/"��]�짏���O/../�>����lE�X���@�c��\-@����v�LT2�2��\�e�� ���l�+���G�6������"�%�z<.��g�������     