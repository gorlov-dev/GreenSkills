"""version tables

Revision ID: 6b69de32ec8b
Revises: 0b2b106265f7
Create Date: 2025-02-02 14:58:44.277225

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6b69de32ec8b"
down_revision = "0b2b106265f7"
branch_labels = None
depends_on = None


def upgrade():
    # Таблицы версий
    op.execute(
        """
        CREATE TABLE presentations_versions (
            id SERIAL PRIMARY KEY,
            presentation_id INT NOT NULL REFERENCES presentations(id) ON DELETE CASCADE,
            version INT NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
            changes JSONB NOT NULL
        );
    """
    )
    op.execute(
        """
        CREATE TABLE slides_versions (
            id SERIAL PRIMARY KEY,
            slide_id INT NOT NULL REFERENCES slides(id) ON DELETE CASCADE,
            version INT NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
            changes JSONB NOT NULL
        );
    """
    )

    # Функция сравнения JSON объектов
    op.execute(
        """
        CREATE OR REPLACE FUNCTION base.jsonb_diff_recursive(left_jsonb JSONB, right_jsonb JSONB) RETURNS JSONB AS $$
        DECLARE
            result JSONB := '{}';
            key TEXT;
            value JSONB;
            left_value JSONB;
            diff JSONB;
        BEGIN
            -- Перебираем ключи из right_jsonb
            FOR key, value IN (SELECT k, v FROM jsonb_each(right_jsonb) AS x(k, v))
            LOOP
                -- Если ключ отсутствует в left_jsonb, то будет NULL
                left_value := left_jsonb->key;

                -- 🔹 Если это массив, проверяем его содержимое
                IF jsonb_typeof(left_value) = 'array' AND jsonb_typeof(value) = 'array' THEN
                    -- Если массивы разные, записываем новый
                    IF left_value IS DISTINCT FROM value THEN
                        result := jsonb_set(result, ARRAY[key], value);
                    END IF;
                    CONTINUE;
                END IF;

                -- 🔹 Если это объекты, сравниваем рекурсивно
                IF jsonb_typeof(left_value) = 'object' AND jsonb_typeof(value) = 'object' THEN
                    diff := base.jsonb_diff_recursive(left_value, value);
                    IF diff IS NOT NULL AND diff <> '{}' THEN
                        result := jsonb_set(result, ARRAY[key], diff);
                    END IF;
                -- Если значения различаются, добавляем в результат
                ELSIF left_value IS DISTINCT FROM value THEN
                    result := jsonb_set(result, ARRAY[key], value);
                END IF;
            END LOOP;
            
            RETURN result;
        END;
        $$ LANGUAGE plpgsql;
    """
    )

    # Функции сохранения изменений
    op.execute(
        """
        CREATE OR REPLACE FUNCTION base.track_presentation_changes()
        RETURNS TRIGGER AS $$
        DECLARE
            changes JSONB;
        BEGIN
            -- Безопасный вызов jsonb_diff_recursive с защитой от NULL
            changes := COALESCE(base.jsonb_diff_recursive(
                jsonb_build_object(
                    'prompt', NEW.prompt,
                    'title', NEW.title
                ),
                jsonb_build_object(
                    'prompt', OLD.prompt,
                    'title', OLD.title
                )
            ), '{}'::jsonb);

            -- Исправлено условие проверки наличия изменений
            IF jsonb_typeof(changes) = 'object' 
            AND EXISTS (SELECT 1 FROM jsonb_object_keys(changes) LIMIT 1) THEN

                INSERT INTO presentations_versions (presentation_id, version, changes)
                VALUES (OLD.id, OLD.version, changes);

                -- Проверка на UPDATE, чтобы избежать рекурсии
                IF TG_OP = 'UPDATE' THEN
                    UPDATE presentations SET version = OLD.version + 1 WHERE id = OLD.id;
                END IF;
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """
    )
    op.execute(
        """
        CREATE OR REPLACE FUNCTION base.track_slide_changes()
        RETURNS TRIGGER AS $$
        DECLARE
            changes JSONB;
        BEGIN
            -- Безопасный вызов jsonb_diff_recursive с защитой от NULL
            changes := COALESCE(base.jsonb_diff_recursive(
                jsonb_build_object(
                    'prompt', NEW.prompt,
                    'data', NEW.data,
                    'position', NEW.position,
                    'template_id', NEW.template_id
                ),
                jsonb_build_object(
                    'prompt', OLD.prompt,
                    'data', OLD.data,
                    'position', OLD.position,
                    'template_id', OLD.template_id
                )
            ), '{}'::jsonb);

            -- Исправлено условие проверки наличия изменений
            IF jsonb_typeof(changes) = 'object' 
            AND EXISTS (SELECT 1 FROM jsonb_object_keys(changes) LIMIT 1) THEN

                INSERT INTO slides_versions (slide_id, version, changes)
                VALUES (OLD.id, OLD.version, changes);

                -- Проверка на UPDATE, чтобы избежать рекурсии
                IF TG_OP = 'UPDATE' THEN
                    UPDATE slides SET version = OLD.version + 1 WHERE id = OLD.id;
                END IF;
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

    """
    )
    op.execute(
        """
        CREATE TRIGGER presentations_versioning
        AFTER UPDATE ON presentations
        FOR EACH ROW
        WHEN (OLD IS DISTINCT FROM NEW)
        EXECUTE FUNCTION base.track_presentation_changes(); 
            """
    )
    op.execute(
        """
        CREATE TRIGGER slides_versioning
        AFTER UPDATE ON slides
        FOR EACH ROW
        WHEN (OLD IS DISTINCT FROM NEW)
        EXECUTE FUNCTION base.track_slide_changes();
            """
    )


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS presentations_versioning ON presentations;")
    op.execute("DROP TRIGGER IF EXISTS slides_versioning ON slides;")
    op.execute("DROP FUNCTION IF EXISTS base.track_presentation_changes;")
    op.execute("DROP FUNCTION IF EXISTS base.track_slide_changes;")
    op.execute("DROP FUNCTION IF EXISTS base.jsonb_diff_recursive;")
    op.execute("DROP TABLE IF EXISTS presentations_versions;")
    op.execute("DROP TABLE IF EXISTS slides_versions;")
